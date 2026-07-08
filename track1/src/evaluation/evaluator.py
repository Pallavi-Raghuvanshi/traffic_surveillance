# ============================================================================
# evaluator.py
# ============================================================================

from __future__ import annotations

from statistics import mean

from core.schemas import Detection
from core.schemas import Track

from evaluation.benchmark_summary import (
    BenchmarkSummary,
)


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
    # Console
    # ------------------------------------------------------------------ #

    def print_summary(
        self,
        summary: BenchmarkSummary,
    ) -> None:

        print()

        print("=" * 60)

        print("Evaluation Summary")

        print("=" * 60)

        print(
            f"Frames Processed        : "
            f"{summary.frames_processed}"
        )

        print(
            f"Average FPS             : "
            f"{summary.average_fps:.2f}"
        )

        print(
            f"Average Processing Time : "
            f"{summary.average_processing_time_ms:.2f} ms"
        )

        print(
            f"Average Detections      : "
            f"{summary.average_detections:.2f}"
        )

        print(
            f"Average Tracks          : "
            f"{summary.average_tracks:.2f}"
        )

        print(
            f"Average Speed           : "
            f"{summary.average_speed:.2f} km/h"
        )

        print("=" * 60)