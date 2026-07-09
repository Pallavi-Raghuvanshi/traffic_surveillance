from __future__ import annotations

import numpy as np


class SimilarityEngine:
    """
    Computes similarity between vehicle embeddings.
    """

    @staticmethod
    def l2_normalize(
        embedding: np.ndarray,
    ) -> np.ndarray:
        """
        L2-normalize an embedding vector.
        """

        norm = np.linalg.norm(embedding)

        if norm == 0:
            raise ValueError("Cannot normalize a zero vector.")

        return embedding / norm

    @staticmethod
    def cosine_similarity(
        embedding_a: np.ndarray,
        embedding_b: np.ndarray,
    ) -> float:
        """
        Compute cosine similarity between two embeddings.
        """

        embedding_a = SimilarityEngine.l2_normalize(embedding_a)
        embedding_b = SimilarityEngine.l2_normalize(embedding_b)

        similarity = np.dot(
            embedding_a,
            embedding_b,
        )

        return float(similarity)

    @staticmethod
    def euclidean_distance(
        embedding_a: np.ndarray,
        embedding_b: np.ndarray,
    ) -> float:
        """
        Compute Euclidean distance between two embeddings.
        """

        distance = np.linalg.norm(
            embedding_a - embedding_b
        )

        return float(distance)

    @staticmethod
    def top_k(
        query_embedding: np.ndarray,
        gallery_embeddings: np.ndarray,
        k: int = 5,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Return indices and cosine similarities of the top-k
        most similar embeddings.
        """

        query_embedding = SimilarityEngine.l2_normalize(
            query_embedding
        )

        gallery_embeddings = np.asarray(
            [
                SimilarityEngine.l2_normalize(embedding)
                for embedding in gallery_embeddings
            ]
        )

        scores = gallery_embeddings @ query_embedding

        indices = np.argsort(scores)[::-1][:k]

        return indices, scores[indices]