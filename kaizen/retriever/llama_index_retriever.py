import os
import logging
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.schema import TextNode
from kaizen.retriever.custom_vector_store import CustomPGVectorStore
from sqlalchemy import create_engine, text
from llama_index.llms.litellm import LiteLLM
import networkx as nx
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import tiktoken
from kaizen.llms.provider import LLMProvider
from kaizen.retriever.code_chunker import chunk_code
import traceback
from llama_index.embeddings.litellm import LiteLLMEmbedding
from llama_index.core import QueryBundle


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize tokenizer
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


class RepositoryAnalyzer:
    def __init__(self, repo_id=1):
        logger.info("Initializing RepositoryAnalyzer")
        self.engine = create_engine(
            f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}",
            pool_size=10,
            max_overflow=20,
        )
        self.repo_id = repo_id
        self.graph = nx.DiGraph()
        self.vector_store = CustomPGVectorStore.from_params(
            database=os.environ["POSTGRES_DB"],
            host=os.environ["POSTGRES_HOST"],
            password=os.environ["POSTGRES_PASSWORD"],
            port=os.environ["POSTGRES_PORT"],
            user=os.environ["POSTGRES_USER"],
            table_name="embeddings",
            embed_dim=1536,
        )
        self.llm_provider = LLMProvider()
        self.llm = LiteLLM(model_name="small", router=self.llm_provider.provider)
        # embed_llm = LiteLLM(model_name="embedding", router=self.llm_provider.provider)
        self.embed_model = LiteLLMEmbedding(
            model_name="azure/text-embedding-3-small", router=self.llm_provider.provider
        )
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        logger.info("RepositoryAnalyzer initialized successfully")

    def setup_repository(self, repo_path: str):
        self.total_usage = self.llm_provider.DEFAULT_USAGE
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
                    logger.error(traceback.format_exc())
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
            logger.error(traceback.format_exc())

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

        if isinstance(code_info, str):
            code = code_info
        elif isinstance(code_info, dict) and "code" in code_info:
            code = code_info["code"]
        else:
            logger.error(
                f"Unexpected code_info format for {section} - {name}: {type(code_info)}"
            )
            return  # Skip this code block

        language = self.get_language_from_extension(file_path)
        abstraction, usage = self.generate_abstraction(code, language)

        function_id = self.store_code_in_db(code, abstraction, file_path, section, name)
        self.store_abstraction_and_embedding(function_id, abstraction)

        if section == "functions":
            self.analyze_function_calls(name, code)
        logger.debug(f"Finished processing code block: {section} - {name}")

    def store_abstraction_and_embedding(self, function_id: int, abstraction: str):
        logger.debug(
            f"Storing abstraction and embedding for function_id: {function_id}"
        )

        embedding, emb_usage = self.llm_provider.get_text_embedding(abstraction)
        embedding = embedding[0]["embedding"]
        # Store the embedding in the database
        # TODO: DONT PUSH DUPLICATE
        with self.engine.begin() as connection:
            embedding_query = text(
                """
                INSERT INTO function_embeddings (function_id, vector)
                VALUES (:function_id, :vector)
                ON CONFLICT (function_id) DO UPDATE SET vector = EXCLUDED.vector
                """
            )
            connection.execute(
                embedding_query,
                {
                    "function_id": function_id,
                    "vector": embedding,
                },
            )

        # Create a TextNode for the vector store
        # Include repo_id in the metadata
        metadata = {"repo_id": self.repo_id}
        node = TextNode(
            text=abstraction,
            id_=str(function_id),
            embedding=embedding,
            metadata=metadata,
        )

        # Add the node to the vector store
        self.vector_store.add(nodes=[node])

        logger.debug(f"Abstraction and embedding stored for function_id: {function_id}")

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
            abstraction, usage = self.llm_provider.chat_completion(
                prompt="",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert programmer tasked with generating comprehensive and accurate abstractions of code snippets.",
                    },
                    {"role": "user", "content": prompt},
                ],
                custom_model={"max_tokens": adjusted_max_tokens, "model": "small"},
            )
            return abstraction, usage

        except Exception as e:
            raise e

    def ensure_repository_exists(
        self, repo_name, repo_owner, repo_url, repo_description=""
    ):
        with self.engine.begin() as connection:
            repo_query = text(
                """
                INSERT INTO repositories (repo_name, repo_owner, repo_url, repo_description)
                VALUES (:repo_name, :repo_owner, :repo_url, :repo_description)
                ON CONFLICT (repo_name, repo_owner) DO UPDATE SET
                    repo_url = EXCLUDED.repo_url,
                    repo_description = EXCLUDED.repo_description
                RETURNING repo_id
            """
            )
            repo_id = connection.execute(
                repo_query,
                {
                    "repo_name": repo_name,
                    "repo_owner": repo_owner,
                    "repo_url": repo_url,
                    "repo_description": repo_description,
                },
            ).scalar_one()
        return repo_id

    def store_code_in_db(
        self, code: str, abstraction: str, file_path: str, section: str, name: str
    ) -> int:
        logger.debug(f"Storing code in DB: {file_path} - {section} - {name}")
        with self.engine.begin() as connection:
            # Insert into files table (assuming this part is already correct)
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
                    "repo_id": self.repo_id,
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_ext": os.path.splitext(file_path)[1],
                    "programming_language": self.get_language_from_extension(file_path),
                },
            ).scalar_one()

            # Insert into function_abstractions table
            function_query = text(
                """
                INSERT INTO function_abstractions 
                (file_id, function_name, function_signature, abstract_functionality, start_line, end_line)
                VALUES (:file_id, :function_name, :function_signature, :abstract_functionality, :start_line, :end_line)
                RETURNING function_id
                """
            )
            function_id = connection.execute(
                function_query,
                {
                    "file_id": file_id,
                    "function_name": name,
                    "function_signature": "",  # You might want to extract this from the code
                    "abstract_functionality": abstraction,
                    "start_line": 1,  # You might want to calculate actual start and end lines
                    "end_line": len(code.splitlines()),
                },
            ).scalar_one()

        logger.debug(f"Code stored in DB with function_id: {function_id}")
        return function_id

    def store_function_relationships(self):
        logger.info("Storing function relationships")
        with self.engine.begin() as connection:
            for caller, callee in self.graph.edges():
                query = text(
                    """
                    INSERT INTO node_relationships (parent_node_id, child_node_id, relationship_type)
                    VALUES (
                        (SELECT node_id FROM syntax_nodes WHERE node_content LIKE :caller),
                        (SELECT node_id FROM syntax_nodes WHERE node_content LIKE :callee),
                        'calls'
                    )
                    ON CONFLICT DO NOTHING
                """
                )
                connection.execute(
                    query, {"caller": f"%{caller}%", "callee": f"%{callee}%"}
                )
        logger.info("Function relationships stored successfully")

    # def query(self, query_text: str, num_results: int = 5) -> List[Dict[str, Any]]:
    #     logger.info(f"Performing query: '{query_text}' for repo_id: {self.repo_id}")

    #     embedding, emb_usage = self.llm_provider.get_text_embedding(query_text)
    #     embedding = embedding[0]["embedding"]

    #     # Use the custom query method
    #     results = self.vector_store.custom_query(embedding, self.repo_id, num_results)

    #     processed_results = []
    #     for result in results:
    #         processed_results.append({
    #             "function_name": result["metadata"].get("function_name", ""),
    #             "abstraction": result["text"],
    #             "file_path": result["metadata"].get("file_path", ""),
    #             "function_signature": result["metadata"].get("function_signature", ""),
    #             "relevance_score": result["similarity"],
    #         })

    #     logger.info(f"Query completed. Found {len(processed_results)} results.")
    #     return processed_results

    def query(self, query_text: str, num_results: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Performing query: '{query_text}' for repo_id: {self.repo_id}")

        index = VectorStoreIndex.from_vector_store(
            self.vector_store, embed_model=self.embed_model, llm=self.llm
        )

        embedding, emb_usage = self.llm_provider.get_text_embedding(query_text)
        embedding = embedding[0]["embedding"]

        # Create a filter to only search within the current repository
        # filter_dict = {"repo_id": self.repo_id}

        query_bundle = QueryBundle(query_str=query_text, embedding=embedding)
        retriever = index.as_retriever(similarity_top_k=num_results)

        # Apply the filter during retrieval
        nodes = retriever.retrieve(query_bundle)  # Add potential filtering

        results = []
        with self.engine.connect() as connection:
            for node in nodes:
                function_id = (
                    node.node.id_
                )  # Assuming we stored function_id as the node id
                query = text(
                    """
                    SELECT fa.function_name, fa.abstract_functionality, f.file_path, fa.function_signature
                    FROM function_abstractions fa
                    JOIN files f ON fa.file_id = f.file_id
                    WHERE fa.function_id = :function_id
                    """
                )
                result = connection.execute(
                    query, {"function_id": function_id}
                ).fetchone()
                if result:
                    results.append(
                        {
                            "function_name": result[0],
                            "abstraction": result[1],
                            "file_path": result[2],
                            "function_signature": result[3],
                            "relevance_score": (
                                node.score if hasattr(node, "score") else 1.0
                            ),
                        }
                    )

        sorted_results = sorted(
            results, key=lambda x: x["relevance_score"], reverse=True
        )
        logger.info(f"Query completed. Found {len(sorted_results)} results.")
        return sorted_results
