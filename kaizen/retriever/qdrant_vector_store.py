from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from qdrant_client.http.exceptions import ResponseHandlingException
import os
import time
import logging


class QdrantVectorStore:
    def __init__(self, collection_name, vector_size, max_retries=3, retry_delay=2):
        self.HOST = os.getenv("QDRANT_HOST", "localhost")
        self.PORT = os.getenv("QDRANT_PORT", "6333")
        self.QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
        self.collection_name = collection_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.client = self._connect_with_retry()
        self._create_collection(vector_size)

    def _connect_with_retry(self):
        for attempt in range(self.max_retries):
            try:
                client = QdrantClient(
                    self.HOST, port=self.PORT, api_key=self.QDRANT_API_KEY
                )
                # Test the connection
                client.get_collections()
                return client
            except ResponseHandlingException as e:
                if attempt < self.max_retries - 1:
                    logging.warning(
                        f"Connection attempt {attempt + 1} failed. Retrying in {self.retry_delay} seconds..."
                    )
                    time.sleep(self.retry_delay)
                else:
                    raise ConnectionError(
                        f"Failed to connect to Qdrant server at {self.HOST}:{self.PORT} after {self.max_retries} attempts"
                    ) from e

    def _create_collection(self, vector_size):
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create or recreate collection: {str(e)}")

    def add(self, nodes):
        points = [
            PointStruct(
                id=node["id"], vector=node["embedding"], payload=node["metadata"]
            )
            for node in nodes
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector, limit=10):
        results = self.client.search(
            collection_name=self.collection_name, query_vector=query_vector, limit=limit
        )
        return results
