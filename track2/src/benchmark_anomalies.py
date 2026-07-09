# ============================================================================
# benchmark_anomalies.py
# ============================================================================

from __future__ import annotations

import csv

from tabulate import tabulate

from core.config import Config

from evaluation.benchmark_summary import (
    AnomalyBenchmarkSummary,
)

from main import main

from utils.file_utils import (
    benchmark_csv_path,
)


class AnomalyBenchmark:
    """
    Benchmarks every configured anomaly-detector set against the same
    track export.

    This class never processes frames itself.

    It only:
        - modifies configuration
        - calls main(config)
        - collects AnomalyBenchmarkSummary
        - prints rankings
    """

    def __init__(
        self,
    ) -> None:

        self.config = Config()

        self.results: list[
            tuple[str, AnomalyBenchmarkSummary]
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

        for detector_set in benchmark_cfg["detector_sets"]:

            name = detector_set["name"]

            detectors = detector_set["detectors"]

            print()

            print("=" * 70)

            print(
                f"Benchmarking : {name} ({', '.join(detectors)})"
            )

            print("=" * 70)

            self.config["anomaly"]["detectors"] = detectors

            benchmark_cfg["experiment_name"] = name

            summary = main(
                self.config
            )

            self.results.append(
                (name, summary)
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

                    "detector_set",

                    "frames_processed",

                    "average_fps",

                    "average_processing_time_ms",

                    "average_tracks",

                    "total_anomalies",

                    "average_confidence",
                ]
            )

            for name, summary in self.results:

                writer.writerow(

                    [

                        name,

                        summary.frames_processed,

                        summary.average_fps,

                        summary.average_processing_time_ms,

                        summary.average_tracks,

                        summary.total_anomalies,

                        summary.average_confidence,
                    ]
                )

    # ------------------------------------------------------------------ #
    # Console Summary
    # ------------------------------------------------------------------ #

    def _print_summary(
        self,
    ) -> None:

        if not self.results:

            print("\nNo benchmark results.")

            return

        ranking = sorted(

            self.results,

            key=lambda item: item[1].average_fps,

            reverse=True,
        )

        table = []

        for rank, (name, summary) in enumerate(

            ranking,

            start=1,
        ):

            table.append(

                [

                    rank,

                    name,

                    summary.frames_processed,

                    f"{summary.average_fps:.2f}",

                    f"{summary.average_processing_time_ms:.2f}",

                    f"{summary.average_tracks:.2f}",

                    summary.total_anomalies,

                    f"{summary.average_confidence:.2f}",
                ]
            )

        print()

        print("ANOMALY BENCHMARK RESULTS\n")

        print(

            tabulate(

                table,

                headers=[

                    "Rank",

                    "Detector Set",

                    "Frames",

                    "FPS",

                    "Time (ms)",

                    "Tracks",

                    "Anomalies",

                    "Confidence",
                ],

                tablefmt="grid",
            )
        )


# ============================================================================
# Entry Point
# ============================================================================

def main_anomaly_benchmark() -> None:

    benchmark = AnomalyBenchmark()

    benchmark.run()


if __name__ == "__main__":

    main_anomaly_benchmark()
