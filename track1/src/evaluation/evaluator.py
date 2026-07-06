# ============================================================================
# evaluator.py
# ============================================================================

from __future__ import annotations

from statistics import mean


class Evaluator:
    """
    Collects statistics while processing a video.
    """

    def __init__(self) -> None:

        self.frames = 0

        self.processing_times = []

        self.num_detections = []

        self.speeds = []

    def update(
        self,
        num_detections: int,
        processing_time: float,
        speeds: list[float],
    ) -> None:

        self.frames += 1

        self.processing_times.append(
            processing_time
        )

        self.num_detections.append(
            num_detections
        )

        self.speeds.extend(
            speeds
        )

    @property
    def average_fps(
        self,
    ) -> float:

        if not self.processing_times:
            return 0.0

        return 1.0 / mean(
            self.processing_times
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

    @property
    def average_detections(
        self,
    ) -> float:

        if not self.num_detections:
            return 0.0

        return mean(
            self.num_detections
        )

    def print_summary(
        self,
    ) -> None:

        print()

        print("=" * 50)

        print("Evaluation Summary")

        print("=" * 50)

        print(
            f"Frames Processed : {self.frames}"
        )

        print(
            f"Average FPS      : {self.average_fps:.2f}"
        )

        print(
            f"Average Detections : {self.average_detections:.2f}"
        )

        print(
            f"Average Speed      : {self.average_speed:.2f} km/h"
        )

        print("=" * 50)