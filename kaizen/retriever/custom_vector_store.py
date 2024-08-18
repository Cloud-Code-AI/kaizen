from llama_index.vector_stores.postgres import PGVectorStore
from typing import List
import numpy as np
from psycopg2.extras import Json


class CustomPGVectorStore(PGVectorStore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the table name in a new attribute
        self.table_name = kwargs.get("table_name", "embeddings")

    def custom_query(
        self, query_embedding: List[float], repo_id: int, similarity_top_k: int
    ) -> List[dict]:
        # Normalize the query embedding
        query_embedding_np = np.array(query_embedding)
        query_embedding_normalized = query_embedding_np / np.linalg.norm(
            query_embedding_np
        )

        # SQL query with repo_id filter and cosine similarity
        query = f"""
        SELECT 
            e.node_id,
            e.text,
            e.metadata,
            1 - (e.embedding <=> %s::vector) as similarity
        FROM 
            {self.table_name} e
        JOIN 
            function_abstractions fa ON e.node_id = fa.function_id::text
        JOIN 
            files f ON fa.file_id = f.file_id
        WHERE 
            f.repo_id = %s
        ORDER BY 
            similarity DESC
        LIMIT 
            %s
        """

        with self.get_client() as client:
            with client.cursor() as cur:
                cur.execute(
                    query,
                    (query_embedding_normalized.tolist(), repo_id, similarity_top_k),
                )
                results = cur.fetchall()

        return [
            {
                "id": row[0],
                "text": row[1],
                "metadata": row[2] if isinstance(row[2], dict) else Json(row[2]),
                "similarity": row[3],
            }
            for row in results
        ]
