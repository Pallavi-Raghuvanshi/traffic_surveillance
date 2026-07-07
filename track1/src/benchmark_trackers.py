# ============================================================================
# benchmark_trackers.py
# ============================================================================

from __future__ import annotations

import csv

from core.config import Config

from evaluation.benchmark_summary import (
    BenchmarkSummary,
)

from main import main

from utils.file_utils import (
    benchmark_csv_path,
)


class TrackerBenchmark:
    """
    Benchmarks all configured trackers.

    This class never processes video frames.

    It only:
        - modifies configuration
        - calls main(config)
        - collects BenchmarkSummary
        - prints rankings
    """

    def __init__(
        self,
    ) -> None:

        self.config = Config()

        self.results: list[
            tuple[str, BenchmarkSummary]
        ] = []

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(
        self,
    ) -> None:

        benchmark_cfg = (
            self.config["benchmark"]
        )

        benchmark_cfg["enabled"] = True

        benchmark_cfg["type"] = "tracker"

        detector_cfg = (
            benchmark_cfg["detector"]
        )

        self.config["detection"][
            "algorithm"
        ] = detector_cfg[
            "algorithm"
        ]

        self.config["detection"][
            "model"
        ] = detector_cfg[
            "model"
        ]

        for tracker in benchmark_cfg[
            "trackers"
        ]:

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

            summary = main(
                self.config
            )

            self.results.append(
                (
                    tracker,
                    summary,
                )
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
            encoding="utf-8",
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow(

                [

                    "tracker",

                    "frames_processed",

                    "average_fps",

                    "average_processing_time_ms",

                    "average_detections",

                    "average_tracks",

                    "average_speed",
                ]
            )

            for (
                tracker,
                summary,
            ) in self.results:

                writer.writerow(

                    [

                        tracker,

                        summary.frames_processed,

                        summary.average_fps,

                        summary.average_processing_time_ms,

                        summary.average_detections,

                        summary.average_tracks,

                        summary.average_speed,
                    ]
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

            key=lambda item: (

                item[1].average_fps,

                item[1].average_tracks,
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

        for (
            tracker,
            summary,
        ) in ranking:

            print(

                f"{tracker:<20}"

                f"{summary.average_fps:>10.2f}"

                f"{summary.average_processing_time_ms:>14.2f}"

                f"{summary.average_detections:>14.2f}"

                f"{summary.average_tracks:>12.2f}"

                f"{summary.average_speed:>10.2f}"
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