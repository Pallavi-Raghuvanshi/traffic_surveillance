# ============================================================================
# benchmark.py
# ============================================================================

from __future__ import annotations

import csv
from pathlib import Path


class Benchmark:

    def __init__(
        self,
        output_file: str,
    ) -> None:

        self.output_file = Path(
            output_file
        )

    def save(
        self,
        experiment_name: str,
        detector: str,
        tracker: str,
        speed_estimator: str,
        fps: float,
    ) -> None:

        file_exists = (
            self.output_file.exists()
        )

        with self.output_file.open(
            "a",
            newline="",
        ) as csvfile:

            writer = csv.writer(
                csvfile
            )

            if not file_exists:

                writer.writerow(
                    [
                        "Experiment",
                        "Detector",
                        "Tracker",
                        "Speed",
                        "FPS",
                    ]
                )

            writer.writerow(
                [
                    experiment_name,
                    detector,
                    tracker,
                    speed_estimator,
                    fps,
                ]
            )