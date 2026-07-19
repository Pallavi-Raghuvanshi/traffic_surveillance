# ============================================================================
# benchmark_detectors.py
# Section 1 / 3
# Imports + DetectorBenchmark + run()
# ============================================================================

from __future__ import annotations
import csv
from pathlib import Path
from tabulate import tabulate

from core.config import Config
from evaluation.benchmark_summary import BenchmarkSummary
from main import main
from utils.file_utils import benchmark_csv_path

class DetectorBenchmark:
    """
    Responsibilities
    ----------------
    - Modify configuration
    - Call main(config)
    - Collect BenchmarkSummary
    - Export results
    - Print rankings
    """

    def __init__(self) -> None:
        self.config = Config("config.yaml")
        self.results: list[tuple[str, BenchmarkSummary]] = []

    # Run
    def run(self) -> None:

        benchmark_cfg = (self.config["benchmark"])
        benchmark_cfg["enabled"] = True
        benchmark_cfg["type"] = "detector"

        for detector_cfg in benchmark_cfg["detectors"]:

            algorithm = detector_cfg["algorithm"]
            backend = detector_cfg.get("backend")
            print('=====================backend: ', backend)
            model = detector_cfg["model"]

            if model is None:
                experiment_name = backend if backend else algorithm
            else:
                experiment_name = Path(model).stem

            print()
            print("=" * 70)
            if backend:
                print(f"Benchmarking : {backend.upper()} ({experiment_name})")
            else:
                print(f"Benchmarking : {algorithm} ({experiment_name})")
            print("=" * 70)

            self.config["detection"]["algorithm"] = algorithm
            self.config["detection"]["backend"] = backend
            self.config["detection"]["model"] = model
            benchmark_cfg["experiment_name"] = experiment_name
            summary = main(self.config)
            self.results.append((experiment_name, summary))

        self._save_summary()
        self._print_summary()
    
    def _save_summary(self) -> None:

        output_file = benchmark_csv_path(self.config["benchmark"]["output_directory"], "detector")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "detector",
                    "frames_processed",
                    "average_fps",
                    "average_processing_time_ms",
                    "average_detections",
                    "average_tracks",
                    "average_speed",
                ]
            )

            for (detector, summary) in self.results:
                writer.writerow(
                    [
                        detector,
                        summary.frames_processed,
                        summary.average_fps,
                        summary.average_processing_time_ms,
                        summary.average_detections,
                        summary.average_tracks,
                        summary.average_speed,
                    ]
                )

    # Console Summary
    def _print_summary(self) -> None:
        if not self.results:
            print("\nNo benchmark results.")
            return

        ranking = sorted(
            self.results,
            key=lambda item: (
                item[1].average_fps,
                item[1].average_detections,
            ),
            reverse=True,
        )

        table: list[list[str | int]] = []

        for rank, (detector, summary) in enumerate(ranking, start=1):
            table.append(
                [
                    rank,
                    detector,
                    summary.frames_processed,
                    f"{summary.average_fps:.2f}",
                    f"{summary.average_processing_time_ms:.2f}",
                    f"{summary.average_detections:.2f}",
                    f"{summary.average_tracks:.2f}",
                    f"{summary.average_speed:.2f}",
                ]
            )
        print()
        print("DETECTOR BENCHMARK RESULTS\n")
        print(
            tabulate(
                table,
                headers=[
                    "Rank",
                    "Detector",
                    "Frames",
                    "FPS",
                    "Time (ms)",
                    "Detections",
                    "Tracks",
                    "Speed",
                ],
                tablefmt="fancy_grid",
            )
        )

# Entry Point
def main_detector_benchmark() -> None:
    benchmark = DetectorBenchmark()
    benchmark.run()

if __name__ == "__main__":
    main_detector_benchmark()