# ============================================================================
# homography.py
# ============================================================================
# Computes homography matrices and projects image coordinates
# onto the ground plane.
# ============================================================================

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


class Homography:
    """
    Represents a homography transformation between
    image coordinates and world coordinates.
    """

    def __init__(
        self,
        matrix: np.ndarray,
    ) -> None:

        matrix = np.asarray(
            matrix,
            dtype=np.float32,
        )

        if matrix.shape != (3, 3):

            raise ValueError(
                "Homography matrix must be 3x3."
            )

        self._matrix = matrix

    # ------------------------------------------------------------------ #
    # Factory Methods
    # ------------------------------------------------------------------ #

    @classmethod
    def from_points(
        cls,
        image_points: np.ndarray,
        world_points: np.ndarray,
    ) -> "Homography":

        image_points = np.asarray(
            image_points,
            dtype=np.float32,
        )

        world_points = np.asarray(
            world_points,
            dtype=np.float32,
        )

        if len(image_points) != len(world_points):

            raise ValueError(
                "Point correspondence mismatch."
            )

        if len(image_points) < 4:

            raise ValueError(
                "At least four point correspondences "
                "are required."
            )

        matrix, _ = cv2.findHomography(

            image_points,

            world_points,

            method=0,
        )

        if matrix is None:

            raise RuntimeError(
                "Failed to compute homography."
            )

        return cls(
            matrix
        )

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> "Homography":

        path = Path(
            path
        )

        if not path.exists():

            raise FileNotFoundError(
                path
            )

        matrix = np.load(
            path
        )

        return cls(
            matrix
        )

    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #

    def save(
        self,
        path: str | Path,
    ) -> None:

        path = Path(
            path
        )

        path.parent.mkdir(

            parents=True,

            exist_ok=True,
        )

        np.save(

            path,

            self._matrix,
        )

    # ------------------------------------------------------------------ #
    # Projection
    # ------------------------------------------------------------------ #

    def project(
        self,
        point: np.ndarray,
    ) -> np.ndarray:

        point = np.asarray(

            point,

            dtype=np.float32,
        )

        point = point.reshape(
            -1,
            1,
            2,
        )

        projected = cv2.perspectiveTransform(

            point,

            self._matrix,
        )

        return projected.reshape(
            -1,
            2,
        )

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def matrix(
        self,
    ) -> np.ndarray:

        return self._matrix.copy()