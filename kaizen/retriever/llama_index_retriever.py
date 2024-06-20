from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap
from .utils import load_data_from_postgres
from sqlalchemy import make_url
import os

class LlamaIndexRetriever:
    def __init__(self, database_config):
        self.database_config = database_config
        self.index = None

    def load_index(self, folder_path):
        # Load data from a folder
        documents = SimpleDirectoryReader(folder_path).load_data()

        vector_store = PGVectorStore.from_params(
            database=os.environ["db_name"],
            host=os.environ["PG_HOST"],
            password=os.environ["PG_PASSWORD"],
            port=os.environ["PG_PORT"],
            user=os.environ["PG_USER"],
            table_name="embeddings",
            embed_dim=1536,  # openai embedding dimension
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )
        query_engine = index.as_query_engine()

    def query(self, query_text):
        # Perform retrieval using the index
        response = self.index.query(query_text)
        return response