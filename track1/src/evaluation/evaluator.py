# ============================================================================
# evaluator.py
# ============================================================================

from __future__ import annotations

import time

import numpy as np


class Evaluator:
    """
    Collects evaluation statistics for the complete pipeline.

    Metrics
    -------
    Detection FPS

    Average Inference Time

    Total Frames

    Total Detections

    Average Speed
    """

    def __init__(self) -> None:

        self.total_frames = 0

        self.total_detections = 0

        self.total_processing_time = 0.0

        self.speed_measurements: list[float] = []

    def update(
        self,
        num_detections: int,
        processing_time: float,
        speeds: list[float],
    ) -> None:

        self.total_frames += 1

        self.total_detections += num_detections

        self.total_processing_time += processing_time

        self.speed_measurements.extend(speeds)

    @property
    def fps(self) -> float:

        if self.total_processing_time == 0:
            return 0.0

        return self.total_frames / self.total_processing_time

    @property
    def average_processing_time(self) -> float:

        if self.total_frames == 0:
            return 0.0

        return self.total_processing_time / self.total_frames

    @property
    def average_speed(self) -> float:

        if not self.speed_measurements:
            return 0.0

        return float(
            np.mean(
                self.speed_measurements
            )
        )

    def summary(self) -> dict:

        return {

            "frames": self.total_frames,

            "detections": self.total_detections,

            "fps": round(self.fps, 2),

            "avg_processing_time": round(
                self.average_processing_time,
                4,
            ),

            "avg_speed": round(
                self.average_speed,
                2,
            ),
        }

    def print_summary(self) -> None:

        summary = self.summary()

        print()

        print("=" * 45)

        print("TRACK 1 EVALUATION")

        print("=" * 45)

        for key, value in summary.items():

            print(f"{key:25}: {value}")

        print("=" * 45)