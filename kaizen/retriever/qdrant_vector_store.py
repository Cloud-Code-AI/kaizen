from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct


class QdrantVectorStore:
    def __init__(self, collection_name, vector_size):
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = collection_name
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def add(self, nodes):
        points = [
            PointStruct(id=node.id_, vector=node.embedding, payload=node.metadata)
            for node in nodes
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector, limit=10):
        results = self.client.search(
            collection_name=self.collection_name, query_vector=query_vector, limit=limit
        )
        return results
