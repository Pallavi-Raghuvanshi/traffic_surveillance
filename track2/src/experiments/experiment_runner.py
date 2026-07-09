# ============================================================================
# experiment_runner.py
# ============================================================================

from __future__ import annotations

from pathlib import Path

from core.config import Config

from engine.anomaly_engine import AnomalyEngine

from evaluation.benchmark_summary import AnomalyBenchmarkSummary
from evaluation.evaluator import AnomalyEvaluator
from evaluation.metrics import Metrics
from evaluation.metrics_exporter import MetricsExporter

from input.recorded_track_source import RecordedTrackSource
from input.video_loader import VideoLoader

from pipeline import Pipeline

from utils.file_utils import (
    events_csv_path,
    events_json_path,
    metrics_csv_path,
    metrics_json_path,
    video_output_path,
)

from visualization.anomaly_visualizer import AnomalyVisualizer


class ExperimentRunner:
    """
    Composition Root.

    Responsible for creating every object required by the application
    and wiring dependencies together.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.config = config

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(
        self,
    ) -> AnomalyBenchmarkSummary:

        # --------------------------------------------------------------
        # Track Source (Component 1 output)
        # --------------------------------------------------------------

        track_source = RecordedTrackSource(

            self.config["paths"]["tracks_export"],

            fps=self.config["input"]["fps"],
        )

        # --------------------------------------------------------------
        # Anomaly Engine
        # --------------------------------------------------------------

        engine = AnomalyEngine(
            self.config
        )

        # --------------------------------------------------------------
        # Metrics / Evaluation
        # --------------------------------------------------------------

        metrics = Metrics()

        evaluator = AnomalyEvaluator()

        metrics_exporter = MetricsExporter()

        # --------------------------------------------------------------
        # Benchmark Configuration
        # --------------------------------------------------------------

        benchmark_cfg = self.config["benchmark"]

        benchmark_enabled = benchmark_cfg.get(
            "enabled",
            False,
        )

        experiment_name = (
            benchmark_cfg.get("experiment_name")
            or "default"
        )

        # --------------------------------------------------------------
        # Visualizer (only active when a source video is available)
        # --------------------------------------------------------------

        video_loader: VideoLoader | None = None

        visualizer = AnomalyVisualizer(
            highlight_seconds=(
                self.config["visualization"]["highlight_seconds"]
            ),
        )

        video_path = Path(
            self.config["paths"]["video"]
        )

        if benchmark_cfg.get("save_video", False) and video_path.exists():

            video_loader = VideoLoader(
                video_path
            )

            visualizer = AnomalyVisualizer(

                highlight_seconds=(
                    self.config["visualization"]["highlight_seconds"]
                ),

                output_video=video_output_path(
                    benchmark_cfg["output_directory"],
                    experiment_name,
                ),

                fps=video_loader.fps,

                frame_width=video_loader.width,

                frame_height=video_loader.height,

                video_crf=self.config["visualization"]["video_crf"],

                video_preset=self.config["visualization"]["video_preset"],
            )

        # --------------------------------------------------------------
        # Pipeline
        # --------------------------------------------------------------

        pipeline = Pipeline(

            track_source=track_source,

            engine=engine,

            metrics=metrics,

            evaluator=evaluator,

            visualizer=visualizer,

            video_loader=video_loader,
        )

        summary = pipeline.run()

        # --------------------------------------------------------------
        # Export
        # --------------------------------------------------------------

        if benchmark_enabled:

            output_root = benchmark_cfg["output_directory"]

            if benchmark_cfg.get("save_csv", True):

                metrics_exporter.export_summary(
                    summary,
                    csv_path=metrics_csv_path(output_root, experiment_name),
                )

                metrics_exporter.export_events(
                    evaluator.events,
                    csv_path=events_csv_path(output_root, experiment_name),
                )

            if benchmark_cfg.get("save_json", True):

                metrics_exporter.export_summary(
                    summary,
                    json_path=metrics_json_path(output_root, experiment_name),
                )

                metrics_exporter.export_events(
                    evaluator.events,
                    json_path=events_json_path(output_root, experiment_name),
                )

        return summary
