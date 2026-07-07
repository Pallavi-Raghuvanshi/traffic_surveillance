# ============================================================================
# detector_metrics.py
# ============================================================================

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import csv
import json


class DetectorMetrics:
    """
    Collects detector benchmarking statistics.

    Outputs
    -------
    detections.csv
    metrics.json
    """

    def __init__(
        self,
    ) -> None:

        self.frames_processed = 0

        self.total_detections = 0

        self.total_inference_time = 0.0

        self.frame_results: list[dict] = []

    def update(
        self,
        frame_number: int,
        inference_time: float,
        detections: list,
    ) -> None:

        self.frames_processed += 1

        self.total_detections += len(
            detections
        )

        self.total_inference_time += (
            inference_time
        )

        self.frame_results.append(
            {
                "frame": frame_number,
                "detections": len(
                    detections
                ),
                "inference_time_ms":
                    inference_time * 1000,
            }
        )

    @property
    def average_fps(
        self,
    ) -> float:

        if self.total_inference_time == 0:

            return 0.0

        return (
            self.frames_processed
            / self.total_inference_time
        )

    @property
    def average_detections(
        self,
    ) -> float:

        if self.frames_processed == 0:

            return 0.0

        return (
            self.total_detections
            / self.frames_processed
        )

    @property
    def average_inference_time_ms(
        self,
    ) -> float:

        if self.frames_processed == 0:

            return 0.0

        return (
            self.total_inference_time
            / self.frames_processed
            * 1000
        )

    def save_csv(
        self,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        with output_path.open(
            "w",
            newline="",
        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=[
                    "frame",
                    "detections",
                    "inference_time_ms",
                ],
            )

            writer.writeheader()

            writer.writerows(
                self.frame_results
            )

    def save_json(
        self,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        summary = {

            "frames_processed":
                self.frames_processed,

            "average_fps":
                round(
                    self.average_fps,
                    2,
                ),

            "average_detections":
                round(
                    self.average_detections,
                    2,
                ),

            "average_inference_time_ms":
                round(
                    self.average_inference_time_ms,
                    2,
                ),
        }

        with output_path.open(
            "w",
        ) as file:

            json.dump(

                summary,

                file,

                indent=4,
            )

    def summary(
        self,
    ) -> dict:

        return {

            "frames_processed":
                self.frames_processed,

            "average_fps":
                round(
                    self.average_fps,
                    2,
                ),

            "average_detections":
                round(
                    self.average_detections,
                    2,
                ),

            "average_inference_time_ms":
                round(
                    self.average_inference_time_ms,
                    2,
                ),
        }