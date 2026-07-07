import os
import faiss
import numpy as np
import logging
from typing import List, Tuple

logger = logging.getLogger("ai_study_pal")

class FAISSStore:
    """
    Wrapper around FAISS for efficient similarity search of document chunks.
    """
    def __init__(self, dimension: int = 384, index_path: str = "faiss_index.bin"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = self._load_or_create_index()
        # Mapping from FAISS ID (integer) to Document/Chunk ID
        self.id_mapping = {} 

    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            try:
                index = faiss.read_index(self.index_path)
                logger.info(f"Loaded existing FAISS index with {index.ntotal} vectors.")
                return index
            except Exception as e:
                logger.warning(f"Failed to load FAISS index: {e}. Creating new one.")
        
        # L2 distance (Euclidean). For cosine similarity, vectors should be normalized before adding.
        index = faiss.IndexFlatL2(self.dimension)
        return index

    def save(self):
        """Persist index to disk."""
        faiss.write_index(self.index, self.index_path)

    def add_embeddings(self, embeddings: List[List[float]], chunk_ids: List[int]):
        """
        Add new embeddings to the index.
        """
        if not embeddings:
            return
            
        if len(embeddings) != len(chunk_ids):
            raise ValueError("Mismatched length between embeddings and IDs")

        vectors = np.array(embeddings).astype('float32')
        # Normalize for cosine similarity simulation with L2
        faiss.normalize_L2(vectors)

        start_idx = self.index.ntotal
        self.index.add(vectors)
        
        # Update mappings
        for i, chunk_id in enumerate(chunk_ids):
            self.id_mapping[start_idx + i] = chunk_id
            
        self.save()

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[int, float]]:
        """
        Search for the top_k most similar vectors.
        Returns a list of (chunk_id, distance) tuples.
        """
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1 and idx in self.id_mapping: # -1 means no result
                results.append((self.id_mapping[idx], float(distances[0][i])))

        return results
