import numpy as np

from track3.core.similarity_engine import SimilarityEngine

a = np.random.rand(512).astype(np.float32)
b = np.random.rand(512).astype(np.float32)

print(
    SimilarityEngine.cosine_similarity(a, b)
)

print(
    SimilarityEngine.euclidean_distance(a, b)
)