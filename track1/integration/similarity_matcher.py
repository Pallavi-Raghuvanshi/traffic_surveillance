# ============================================================================
# similarity_matcher.py
# ============================================================================

from __future__ import annotations

import numpy as np


class SimilarityMatcher:
    """
    Computes similarity between two vehicle embeddings.
    """

    @staticmethod
    def cosine_similarity(
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> float:
        """
        Compute cosine similarity.

        Since OSNet embeddings are already L2-normalized,
        cosine similarity is simply the dot product.
        """

        return float(np.dot(embedding1, embedding2))

    @staticmethod
    def is_match(
        similarity: float,
        threshold: float,
    ) -> bool:

        return similarity >= threshold