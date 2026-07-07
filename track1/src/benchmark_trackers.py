# ============================================================================
# benchmark_trackers.py
# ============================================================================

"""
Benchmark all configured trackers.

This script does NOT contain any processing loop.

It only updates the configuration and invokes main(config).
"""

from __future__ import annotations

import csv

from core.config import Config

from main import main

from utils.file_utils import (
    benchmark_csv_path,
)


class TrackerBenchmark:

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

        benchmark_cfg["type"] = "tracker"

        detector_cfg = benchmark_cfg["detector"]

        self.config["detection"][
            "algorithm"
        ] = detector_cfg["algorithm"]

        self.config["detection"][
            "model"
        ] = detector_cfg["model"]

        trackers = benchmark_cfg["trackers"]

        for tracker in trackers:

            print()

            print("=" * 70)

            print(
                f"Benchmarking : {tracker}"
            )

            print("=" * 70)

            self.config["tracking"][
                "algorithm"
            ] = tracker

            benchmark_cfg[
                "experiment_name"
            ] = tracker

            result = main(
                self.config
            )

            if result is None:
                continue

            result["tracker"] = tracker

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

            "tracker",
        )

        with output_file.open(
            "w",
            newline="",
        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=[

                    "tracker",

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
    # Print Summary
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

                result["average_tracks"],
            ),

            reverse=True,
        )

        print()

        print("=" * 90)

        print(
            "TRACKER BENCHMARK SUMMARY"
        )

        print("=" * 90)

        print(

            f"{'Tracker':<20}"

            f"{'FPS':>10}"

            f"{'Time(ms)':>14}"

            f"{'Detections':>14}"

            f"{'Tracks':>12}"

            f"{'Speed':>10}"
        )

        print("-" * 90)

        for result in ranking:

            print(

                f"{result['tracker']:<20}"

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

def main_tracker_benchmark() -> None:

    benchmark = TrackerBenchmark()

    benchmark.run()


if __name__ == "__main__":

    main_tracker_benchmark()