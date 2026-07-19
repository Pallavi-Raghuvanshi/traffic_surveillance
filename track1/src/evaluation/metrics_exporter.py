# metrics_exporter.py
# ============================================================================
# Exports BenchmarkSummary to disk as CSV/JSON or both
# ============================================================================

from __future__ import annotations
from dataclasses import asdict
import csv
import json
from pathlib import Path

from evaluation.benchmark_summary import BenchmarkSummary

class MetricsExporter:

    def export_csv(self, summary: BenchmarkSummary, output_path: str | Path) -> None:
        output_path = Path(output_path) # metrics output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=asdict(summary).keys())
            writer.writeheader() # column names added
            writer.writerow(asdict(summary)) 

    def export_json(self, summary: BenchmarkSummary, output_path: str | Path) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(asdict(summary), file, indent=4)

    def export(
        self,
        summary: BenchmarkSummary,
        *,
        csv_path: str | Path | None = None,
        json_path: str | Path | None = None,
    ) -> None:

        if csv_path is not None:
            self.export_csv(summary, csv_path)

        if json_path is not None:
            self.export_json(summary, json_path)

    def export_benchmark_csv(
        self,
        *,
        experiment_name: str,
        detector: str,
        tracker: str,
        speed_estimator: str,
        summary: BenchmarkSummary,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        file_exists = output_path.exists()

        with output_path.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(
                    [
                        "Experiment",
                        "Detector",
                        "Tracker",
                        # "Speed Estimator",
                        "Average FPS",
                        "Frames Processed",
                        "Avg Processing Time (ms)",
                        "Avg Detections",
                        "Avg Tracks",
                    ]
                )

            writer.writerow(
                [
                    experiment_name,
                    detector,
                    tracker,
                    speed_estimator,
                    summary.average_fps,
                    summary.frames_processed,
                    summary.average_processing_time_ms,
                    summary.average_detections,
                    summary.average_tracks,
                ]
            )