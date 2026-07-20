# ============================================================================
# reid_manager.py
# ============================================================================

from __future__ import annotations


import numpy as np

from integration.similarity_matcher import SimilarityMatcher
from integration.vehicle_database import (
    VehicleDatabase,
    VehicleRecord,
)
from track3.demo.predictor import VehicleReIDPredictor
from track1.integration.schemas import ReIDResult


class ReIDManager:
    """
    Performs vehicle re-identification.

    Pipeline
    --------
    Representative Crop
            ↓
    OSNet Embedding
            ↓
    Similarity Search
            ↓
    Existing Vehicle / New Vehicle
    """

    def __init__(
        self,
        predictor: VehicleReIDPredictor,
        database: VehicleDatabase,
        similarity_threshold: float = 0.80,
    ) -> None:

        self.predictor = predictor

        self.database = database

        self.matcher = SimilarityMatcher()

        self.similarity_threshold = similarity_threshold

    def process(
        self,
        track_id: int,
        crop: np.ndarray,
        frame_number: int,
    ) -> ReIDResult:
        """
        Re-identify a completed vehicle track.
        """

        embedding = self.predictor.embedding_from_crop(crop)

        vehicle, similarity = self._find_best_match(
            embedding,
        )

        #
        # Existing vehicle
        #
        if vehicle is not None and self.matcher.is_match(
            similarity,
            self.similarity_threshold,
        ):

            return ReIDResult(
                track_id=track_id,
                vehicle_id=vehicle.vehicle_id,
                similarity=similarity,
                is_new_vehicle=False,
                frame_number=frame_number,
            )

        #
        # Register new vehicle
        #
        vehicle = self.database.add(
            embedding=embedding,
            crop=crop,
        )

        return ReIDResult(
            track_id=track_id,
            vehicle_id=vehicle.vehicle_id,
            similarity=0.0,
            is_new_vehicle=True,
            frame_number=frame_number,
        )

    def _find_best_match(
        self,
        embedding: np.ndarray,
    ) -> tuple[VehicleRecord | None, float]:
        """
        Find the most similar registered vehicle.
        """

        best_vehicle = None

        best_similarity = -1.0

        for vehicle in self.database:

            similarity = self.matcher.cosine_similarity(
                embedding,
                vehicle.embedding,
            )

            if similarity > best_similarity:

                best_similarity = similarity

                best_vehicle = vehicle

        return best_vehicle, best_similarity
