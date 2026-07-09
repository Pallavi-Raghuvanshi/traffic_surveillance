from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from track3.core.preprocessing import ImagePreprocessor
from track3.models.osnet import OSNetModel


class ReIDService:
    """
    High-level interface for Vehicle Re-Identification.

    Pipeline
    --------
    OpenCV Image
            │
            ▼
    ImagePreprocessor
            │
            ▼
    OSNetModel
            │
            ▼
    L2 Normalization
            │
            ▼
    NumPy Embedding
    """

    def __init__(self) -> None:
        self.preprocessor = ImagePreprocessor()
        self.model = OSNetModel()

    def extract_embedding(self, image: np.ndarray) -> np.ndarray:
        """
        Extract a normalized embedding from a vehicle image.

        Parameters
        ----------
        image
            OpenCV BGR image.

        Returns
        -------
        np.ndarray
            L2-normalized embedding of shape (512,).
        """

        image_tensor = self.preprocessor(image)

        embedding = self.model(image_tensor)


        embedding = embedding.squeeze(0)

        embedding = embedding.cpu().numpy()

        return embedding

    def extract_embeddings(
        self,
        images: list[np.ndarray],
    ) -> np.ndarray:
        """
        Extract embeddings for multiple vehicle images.

        Returns
        -------
        np.ndarray
            Array of shape (N, 512).
        """

        embeddings = [
            self.extract_embedding(image)
            for image in images
        ]

        return np.asarray(embeddings)