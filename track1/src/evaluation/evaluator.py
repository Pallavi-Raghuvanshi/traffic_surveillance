# evaluator.py
# ============================================================================
# Evaluates performance of Detection and Tracking algorithms
# ============================================================================

from __future__ import annotations
from statistics import mean

from src.core.schemas import Detection, Track
from src.evaluation.benchmark_summary import BenchmarkSummary

class Evaluator:

    def __init__(self) -> None:
        self.num_detections: list[int] = []
        self.num_tracks: list[int] = []
        # self.speeds: list[float] = []

    def update(
        self,
        *,
        detections: list[Detection],
        tracks: list[Track],
        # speeds: list[float],
    ) -> None:

        self.num_detections.append(len(detections))
        self.num_tracks.append(len(tracks))
        # self.speeds.extend(speeds)

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def average_detections(self) -> float:
        if not self.num_detections:
            return 0.0
        return mean(self.num_detections)

    @property
    def average_tracks(self) -> float:
        if not self.num_tracks:
            return 0.0
        return mean(self.num_tracks)

    # @property
    # def average_speed(self) -> float:
    #     if not self.speeds:
    #         return 0.0
    #     return mean(self.speeds)

    # ------------------------------------------------------------------ #
    # Console
    # ------------------------------------------------------------------ #

    def print_summary(self, summary: BenchmarkSummary) -> None:
        print()
        print("=" * 60)
        print("Evaluation Summary")
        print("=" * 60)
        print(f"Frames Processed        : {summary.frames_processed}")
        print(f"Average FPS             : {summary.average_fps:.2f}")
        print(f"Average Processing Time : {summary.average_processing_time_ms:.2f} ms")
        print(f"Average Detections      : {summary.average_detections:.2f}")
        print(f"Average Tracks          : {summary.average_tracks:.2f}")
        print(f"Average Speed           : {summary.average_speed:.2f} km/h")
        print("=" * 60)