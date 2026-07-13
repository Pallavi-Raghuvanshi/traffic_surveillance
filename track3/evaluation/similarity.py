from __future__ import annotations

import numpy as np


class Similarity:

    @staticmethod
    def cosine(
        query_embeddings: np.ndarray,
        gallery_embeddings: np.ndarray,
    ) -> np.ndarray:
        """
        Compute cosine similarity matrix.

        Returns
        -------
        (num_queries, num_gallery)
        """

        query_embeddings = (
            query_embeddings
            / np.linalg.norm(
                query_embeddings,
                axis=1,
                keepdims=True,
            )
        )

        gallery_embeddings = (
            gallery_embeddings
            / np.linalg.norm(
                gallery_embeddings,
                axis=1,
                keepdims=True,
            )
        )

        return query_embeddings @ gallery_embeddings.T
    
