# ============================================================================
# evaluator.py
# ============================================================================

from __future__ import annotations

from statistics import mean

from core.schemas import Detection
from core.schemas import Track


class Evaluator:
    """
    Evaluates algorithm performance.

    Responsibilities
    ----------------
    - Detection statistics
    - Tracking statistics
    - Speed statistics

    Runtime statistics such as FPS and processing time
    are collected exclusively by Metrics.
    """

    def __init__(
        self,
    ) -> None:

        self.frames = 0

        self.num_detections: list[int] = []

        self.num_tracks: list[int] = []

        self.speeds: list[float] = []

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        *,
        detections: list[Detection],
        tracks: list[Track],
        speeds: list[float],
    ) -> None:

        self.frames += 1

        self.num_detections.append(
            len(detections)
        )

        self.num_tracks.append(
            len(tracks)
        )

        self.speeds.extend(
            speeds
        )

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def average_detections(
        self,
    ) -> float:

        if not self.num_detections:
            return 0.0

        return mean(
            self.num_detections
        )

    @property
    def average_tracks(
        self,
    ) -> float:

        if not self.num_tracks:
            return 0.0

        return mean(
            self.num_tracks
        )

    @property
    def average_speed(
        self,
    ) -> float:

        if not self.speeds:
            return 0.0

        return mean(
            self.speeds
        )

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def summary(
        self,
    ) -> dict:

        return {

            "frames_processed":
                self.frames,

            "average_detections":
                self.average_detections,

            "average_tracks":
                self.average_tracks,

            "average_speed":
                self.average_speed,
        }

    # ------------------------------------------------------------------ #
    # Console
    # ------------------------------------------------------------------ #

    def print_summary(
        self,
    ) -> None:

        summary = self.summary()

        print()

        print("=" * 60)

        print("EVALUATION SUMMARY")

        print("=" * 60)

        print(
            f"Frames              : "
            f"{summary['frames_processed']}"
        )

        print(
            f"Average Detections  : "
            f"{summary['average_detections']:.2f}"
        )

        print(
            f"Average Tracks      : "
            f"{summary['average_tracks']:.2f}"
        )

        print(
            f"Average Speed       : "
            f"{summary['average_speed']:.2f}"
        )

        print("=" * 60)