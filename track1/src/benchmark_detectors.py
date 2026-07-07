# ============================================================================
# benchmark_detectors.py
# ============================================================================

"""
Benchmark all configured detectors.

This script DOES NOT execute any processing loop.

It simply modifies the configuration and invokes main(config).

Outputs
-------
outputs/
    detector_benchmark/
        detector_results.csv

        yolo11n/
            annotated.mp4
            metrics.csv
            metrics.json

        rtdetr/
            ...

        faster_rcnn/
            ...
"""

from __future__ import annotations

import csv
from pathlib import Path

from core.config import Config

from main import main

from utils.file_utils import (
    benchmark_csv_path,
)


class DetectorBenchmark:

    def __init__(
        self,
    ) -> None:

        self.config = Config()

        self.results: list[dict] = []

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(
        self,
    ) -> None:

        benchmark_cfg = self.config["benchmark"]

        benchmark_cfg["enabled"] = True

        benchmark_cfg["type"] = "detector"

        detectors = benchmark_cfg["detectors"]

        for detector in detectors:

            algorithm = detector["algorithm"]

            model = detector["model"]

            experiment_name = (
                Path(model).stem
            )

            print()

            print("=" * 70)

            print(
                f"Benchmarking : "
                f"{algorithm} "
                f"({experiment_name})"
            )

            print("=" * 70)

            self.config["detection"][
                "algorithm"
            ] = algorithm

            self.config["detection"][
                "model"
            ] = model

            benchmark_cfg[
                "experiment_name"
            ] = experiment_name

            result = main(
                self.config
            )

            if result is None:
                continue

            result["detector"] = (
                experiment_name
            )

            self.results.append(
                result
            )

        self._save_summary()

        self._print_summary()

    # ------------------------------------------------------------------ #
    # Save Summary
    # ------------------------------------------------------------------ #

    def _save_summary(
        self,
    ) -> None:

        output_file = benchmark_csv_path(

            self.config["benchmark"][
                "output_directory"
            ],

            "detector",
        )

        with output_file.open(
            "w",
            newline="",
        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=[

                    "detector",

                    "frames_processed",

                    "average_fps",

                    "average_processing_time_ms",

                    "average_detections",

                    "average_tracks",

                    "average_speed",
                ],
            )

            writer.writeheader()

            writer.writerows(
                self.results
            )

    # ------------------------------------------------------------------ #
    # Console Summary
    # ------------------------------------------------------------------ #

    def _print_summary(
        self,
    ) -> None:

        if not self.results:

            print(
                "\nNo benchmark results."
            )

            return

        ranking = sorted(

            self.results,

            key=lambda result: (

                result["average_fps"],

                result[
                    "average_detections"
                ],
            ),

            reverse=True,
        )

        print()

        print("=" * 90)

        print(
            "DETECTOR BENCHMARK SUMMARY"
        )

        print("=" * 90)

        print(

            f"{'Detector':<30}"

            f"{'FPS':>10}"

            f"{'Time(ms)':>14}"

            f"{'Detections':>14}"

            f"{'Tracks':>12}"

            f"{'Speed':>10}"
        )

        print("-" * 90)

        for result in ranking:

            print(

                f"{result['detector']:<30}"

                f"{result['average_fps']:>10.2f}"

                f"{result['average_processing_time_ms']:>14.2f}"

                f"{result['average_detections']:>14.2f}"

                f"{result['average_tracks']:>12.2f}"

                f"{result['average_speed']:>10.2f}"
            )

        print("=" * 90)


# ============================================================================
# Entry Point
# ============================================================================

def main_detector_benchmark() -> None:

    benchmark = DetectorBenchmark()

    benchmark.run()


if __name__ == "__main__":

    main_detector_benchmark()