import os
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import create_engine, text
import ast
import networkx as nx


class RepositoryAnalyzer:
    def __init__(self):
        self.index = None
        self.engine = create_engine(
            f"postgresql://{os.environ['PG_USER']}:{os.environ['PG_PASSWORD']}@{os.environ['PG_HOST']}:{os.environ['PG_PORT']}/{os.environ['db_name']}"
        )
        self.graph = nx.DiGraph()

    def load_index(self, folder_path):
        documents = SimpleDirectoryReader(folder_path).load_data()

        vector_store = PGVectorStore.from_params(
            database=os.environ["db_name"],
            host=os.environ["PG_HOST"],
            password=os.environ["PG_PASSWORD"],
            port=os.environ["PG_PORT"],
            user=os.environ["PG_USER"],
            table_name="embeddings",
            embed_dim=512,  # openai embedding dimension
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )

    def parse_repository(self, repo_path):
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self.parse_file(file_path)

    def parse_file(self, file_path):
        with open(file_path, "r") as file:
            content = file.read()

        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.process_function(node, file_path)

    def process_function(self, node, file_path):
        function_name = node.name
        start_line = node.lineno
        end_line = node.end_lineno

        # Store function information in the database
        self.store_function_in_db(function_name, file_path, start_line, end_line)

        # Analyze function calls within the function
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Call):
                if isinstance(sub_node.func, ast.Name):
                    called_function = sub_node.func.id
                    self.graph.add_edge(function_name, called_function)

    def store_function_in_db(self, function_name, file_path, start_line, end_line):
        with self.engine.connect() as connection:
            # Insert into files table if not exists
            file_query = text(
                """
                INSERT INTO files (repo_id, file_path, file_name, file_ext, programming_language)
                VALUES (:repo_id, :file_path, :file_name, :file_ext, :programming_language)
                ON CONFLICT (repo_id, file_path) DO UPDATE SET file_path = EXCLUDED.file_path
                RETURNING file_id
            """
            )
            file_result = connection.execute(
                file_query,
                {
                    "repo_id": 1,  # Assuming repo_id is 1, adjust as needed
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_ext": ".py",
                    "programming_language": "Python",
                },
            )
            file_id = file_result.fetchone()[0]

            # Insert into code_snippets table
            snippet_query = text(
                """
                INSERT INTO code_snippets (file_id, snippet_text, start_line, end_line, functionality)
                VALUES (:file_id, :snippet_text, :start_line, :end_line, :functionality)
                RETURNING snippet_id
            """
            )
            snippet_result = connection.execute(
                snippet_query,
                {
                    "file_id": file_id,
                    "snippet_text": function_name,  # This should be the actual function code
                    "start_line": start_line,
                    "end_line": end_line,
                    "functionality": f"Function: {function_name}",
                },
            )
            snippet_id = snippet_result.fetchone()[0]

            # Insert into ast_nodes table
            node_query = text(
                """
                INSERT INTO ast_nodes (file_id, node_type, start_line, end_line)
                VALUES (:file_id, :node_type, :start_line, :end_line)
                RETURNING node_id
            """
            )
            node_result = connection.execute(
                node_query,
                {
                    "file_id": file_id,
                    "node_type": "FunctionDef",
                    "start_line": start_line,
                    "end_line": end_line,
                },
            )
            node_id = node_result.fetchone()[0]

            # Insert function name as a property
            prop_query = text(
                """
                INSERT INTO node_properties (node_id, property_name, property_value)
                VALUES (:node_id, :property_name, :property_value)
            """
            )
            connection.execute(
                prop_query,
                {
                    "node_id": node_id,
                    "property_name": "function_name",
                    "property_value": function_name,
                },
            )

    def store_function_relationships(self):
        for caller, callee in self.graph.edges():
            with self.engine.connect() as connection:
                query = text(
                    """
                    INSERT INTO node_relationships (parent_node_id, child_node_id, relationship_type)
                    VALUES (
                        (SELECT node_id FROM ast_nodes WHERE node_type = 'FunctionDef' AND node_id IN 
                            (SELECT node_id FROM node_properties WHERE property_name = 'function_name' AND property_value = :caller)
                        ),
                        (SELECT node_id FROM ast_nodes WHERE node_type = 'FunctionDef' AND node_id IN 
                            (SELECT node_id FROM node_properties WHERE property_name = 'function_name' AND property_value = :callee)
                        ),
                        'calls'
                    )
                """
                )
                connection.execute(query, {"caller": caller, "callee": callee})

    def query(self, query_text):
        # Perform retrieval using the index
        response = self.index.query(query_text)
        return response

    def analyze_repository(self, repo_path):
        self.parse_repository(repo_path)
        self.store_function_relationships()
        self.load_index(repo_path)
