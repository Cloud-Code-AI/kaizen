import os
import logging
import openai
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    Document,
)
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import create_engine, text
import ast
from llama_index.core import VectorStoreIndex

import networkx as nx
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import tiktoken
from kaizen.llms.provider import LLMProvider
from kaizen.retriever.code_chunker import chunk_code

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize tokenizer
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


class RepositoryAnalyzer:
    def __init__(self):
        logger.info("Initializing RepositoryAnalyzer")
        self.engine = create_engine(
            f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}",
            pool_size=10,
            max_overflow=20,
        )
        self.graph = nx.DiGraph()
        self.vector_store = PGVectorStore.from_params(
            database=os.environ["POSTGRES_DB"],
            host=os.environ["POSTGRES_HOST"],
            password=os.environ["POSTGRES_PASSWORD"],
            port=os.environ["POSTGRES_PORT"],
            user=os.environ["POSTGRES_USER"],
            table_name="embeddings",
            embed_dim=1536,  # OpenAI's text-embedding-ada-002 dimension
        )
        self.provider = LLMProvider()
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        logger.info("RepositoryAnalyzer initialized successfully")

    def setup_repository(self, repo_path: str):
        self.total_usage = self.provider.DEFAULT_USAGE
        logger.info(f"Starting repository setup for: {repo_path}")
        self.parse_repository(repo_path)
        self.store_function_relationships()
        logger.info("Repository setup completed successfully")

    def parse_repository(self, repo_path: str):
        logger.info(f"Parsing repository: {repo_path}")
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []
            for root, _, files in os.walk(repo_path):
                for file in files:
                    if file.endswith(
                        (".py", ".js", ".ts", ".rs")
                    ):  # Add more extensions as needed
                        file_path = os.path.join(root, file)
                        futures.append(executor.submit(self.parse_file, file_path))

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error in parsing file: {str(e)}")
        logger.info("Repository parsing completed")

    def parse_file(self, file_path: str):
        logger.debug(f"Parsing file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            language = self.get_language_from_extension(file_path)
            chunked_code = chunk_code(content, language)

            for section, items in chunked_code.items():
                if isinstance(items, dict):
                    for name, code_info in items.items():
                        self.process_code_block(code_info, file_path, section, name)
                elif isinstance(items, list):
                    for i, code_info in enumerate(items):
                        self.process_code_block(
                            code_info, file_path, section, f"{section}_{i}"
                        )
            logger.debug(f"Successfully parsed file: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")

    @staticmethod
    def get_language_from_extension(file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        return {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".rs": "rust",
        }.get(ext, "unknown")

    def process_code_block(
        self, code_info: Dict[str, Any], file_path: str, section: str, name: str
    ):
        logger.debug(f"Processing code block: {section} - {name}")
        code = code_info["code"]
        language = self.get_language_from_extension(file_path)
        abstraction, usage = self.generate_abstraction(code, language)
        total_usage = self.provider.update_usage()

        snippet_id = self.store_code_in_db(code, abstraction, file_path, section, name)
        self.store_abstraction_and_embedding(snippet_id, abstraction)

        if section == "functions":
            self.analyze_function_calls(name, code)
        logger.debug(f"Finished processing code block: {section} - {name}")

    def generate_abstraction(
        self, code_block: str, language: str, max_tokens: int = 300
    ) -> str:
        prompt = f"""Generate a concise yet comprehensive abstract description of the following {language} code block. 
        Include information about:
        1. The purpose or functionality of the code
        2. Input parameters and return values (if applicable)
        3. Any important algorithms or data structures used
        4. Key dependencies or external libraries used
        5. Any notable design patterns or architectural choices
        6. Potential edge cases or error handling

        Code:
        ```{language}
        {code_block}
        ```
        """

        estimated_prompt_tokens = len(tokenizer.encode(prompt))
        adjusted_max_tokens = min(max(150, estimated_prompt_tokens), 1000)

        try:
            abstraction, usage = self.provider.chat_completion(
                model="small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert programmer tasked with generating comprehensive and accurate abstractions of code snippets.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=adjusted_max_tokens,
                n=1,
                temperature=0.5,
            )
            return abstraction

        except Exception as e:
            raise e

    def store_code_in_db(
        self, code: str, abstraction: str, file_path: str, section: str, name: str
    ) -> int:
        logger.debug(f"Storing code in DB: {file_path} - {section} - {name}")
        with self.engine.begin() as connection:
            file_query = text(
                """
                INSERT INTO files (repo_id, file_path, file_name, file_ext, programming_language)
                VALUES (:repo_id, :file_path, :file_name, :file_ext, :programming_language)
                ON CONFLICT (repo_id, file_path) DO UPDATE SET file_path = EXCLUDED.file_path
                RETURNING file_id
            """
            )
            file_id = connection.execute(
                file_query,
                {
                    "repo_id": 1,  # Assuming repo_id is 1, adjust as needed
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_ext": os.path.splitext(file_path)[1],
                    "programming_language": self.get_language_from_extension(file_path),
                },
            ).scalar_one()

            snippet_query = text(
                """
                INSERT INTO code_snippets (file_id, snippet_text, functionality, context)
                VALUES (:file_id, :snippet_text, :functionality, :context)
                RETURNING snippet_id
            """
            )
            snippet_id = connection.execute(
                snippet_query,
                {
                    "file_id": file_id,
                    "snippet_text": code,
                    "functionality": abstraction,
                    "context": f"{section}: {name}",
                },
            ).scalar_one()

        logger.debug(f"Code stored in DB with snippet_id: {snippet_id}")
        return snippet_id

    def store_abstraction_and_embedding(self, snippet_id: int, abstraction: str):
        logger.debug(f"Storing abstraction and embedding for snippet_id: {snippet_id}")

        embedding = self.provider.get_text_embedding(abstraction)
        doc = Document(text=abstraction, metadata={"snippet_id": snippet_id})
        self.vector_store.add_documents([doc], embedding_vectors=[embedding])

        logger.debug(f"Abstraction and embedding stored for snippet_id: {snippet_id}")

    def analyze_function_calls(self, function_name: str, code: str):
        logger.debug(f"Analyzing function calls for: {function_name}")
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.graph.add_edge(function_name, node.func.id)
                    logger.debug(f"Added edge: {function_name} -> {node.func.id}")
        except SyntaxError:
            logger.error(f"Syntax error in function {function_name}")

    def store_function_relationships(self):
        logger.info("Storing function relationships")
        with self.engine.begin() as connection:
            for caller, callee in self.graph.edges():
                query = text(
                    """
                    INSERT INTO node_relationships (parent_node_id, child_node_id, relationship_type)
                    VALUES (
                        (SELECT snippet_id FROM code_snippets WHERE context LIKE :caller),
                        (SELECT snippet_id FROM code_snippets WHERE context LIKE :callee),
                        'calls'
                    )
                    ON CONFLICT DO NOTHING
                """
                )
                connection.execute(
                    query, {"caller": f"%{caller}", "callee": f"%{callee}"}
                )
        logger.info("Function relationships stored successfully")

    def query(self, query_text: str, num_results: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Performing query: '{query_text}'")

        index = VectorStoreIndex.from_vector_store(self.vector_store)
        
        # Create a query engine
        query_engine = index.as_query_engine(similarity_top_k=num_results)
        
        # Perform the query
        response = query_engine.query(query_text)
        
        results = []
        with self.engine.connect() as connection:
            for node in response.source_nodes:
                snippet_id = node.metadata["snippet_id"]
                query = text("""
                    SELECT cs.snippet_text, cs.functionality, f.file_path
                    FROM code_snippets cs
                    JOIN files f ON cs.file_id = f.file_id
                    WHERE cs.snippet_id = :snippet_id
                """)
                result = connection.execute(query, {"snippet_id": snippet_id}).fetchone()
                if result:
                    results.append({
                        "code": result[0],
                        "abstraction": result[1],
                        "file_path": result[2],
                        "relevance_score": node.score if hasattr(node, 'score') else 1.0
                    })
        
        sorted_results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)
        logger.info(f"Query completed. Found {len(sorted_results)} results.")
        return sorted_results
