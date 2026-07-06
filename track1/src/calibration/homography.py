# ============================================================================
# homography.py
# ============================================================================
# computes homography matrix from corresponding image/world points
# and projects image points into real-world coordinates

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


class Homography:
    """
    Computes and applies homography transformations between
    image coordinates and ground-plane coordinates.
    """

    def __init__(
        self,
        matrix: np.ndarray,
    ) -> None:

        if matrix.shape != (3, 3):
            raise ValueError(
                "Homography matrix must be 3x3."
            )

        self._matrix = matrix.astype(np.float32)

    @classmethod
    def from_points(
        cls,
        image_points: np.ndarray,
        world_points: np.ndarray,
    ) -> "Homography":
        """
        Estimate homography from corresponding points.
        """

        matrix, _ = cv2.findHomography(
            image_points,
            world_points,
            method=0,
        )

        if matrix is None:
            raise RuntimeError(
                "Failed to compute homography."
            )

        return cls(matrix)

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> "Homography":

        path = Path(path)

        matrix = np.load(path)

        return cls(matrix)

    def save(
        self,
        path: str | Path,
    ) -> None:

        np.save(
            Path(path),
            self._matrix,
        )

    def project(
        self,
        point: np.ndarray,
    ) -> np.ndarray:
        """
        Project pixel coordinates to world coordinates.
        """

        point = np.asarray(
            point,
            dtype=np.float32,
        ).reshape(-1, 1, 2)

        projected = cv2.perspectiveTransform(
            point,
            self._matrix,
        )

        return projected.reshape(-1, 2)

    @property
    def matrix(
        self,
    ) -> np.ndarray:

        return self._matrix.copy()