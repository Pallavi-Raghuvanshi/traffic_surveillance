# ============================================================================
# experiment_runner.py
# ============================================================================

from __future__ import annotations

from core.config import Config

from detection.detector_factory import DetectorFactory
from tracking.tracker_factory import TrackerFactory

from speed import (
    SpeedEstimatorFactory,
    TrajectoryManager,
)

from input.video_loader import VideoLoader

from evaluation import Evaluator
from evaluation.metrics import Metrics

from visualization.visualizer import Visualizer

from pipeline import Pipeline

from utils.file_utils import (
    video_output_path,
    csv_output_path,
    json_output_path,
)


class ExperimentRunner:
    """
    Creates and executes a complete experiment.

    Normal execution and benchmarking both use the same pipeline.
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
    ) -> dict | None:

        video_loader = VideoLoader(
            self.config["paths"]["video"]
        )

        detector = DetectorFactory.create(
            self.config
        )

        tracker = TrackerFactory.create(
            self.config
        )

        trajectory_manager = (
            TrajectoryManager()
        )

        speed_estimator = (
            SpeedEstimatorFactory.create(
                self.config,
                fps=video_loader.fps,
            )
        )

        evaluator = Evaluator()

        benchmark_cfg = self.config["benchmark"]

        benchmark_enabled = benchmark_cfg.get(
            "enabled",
            False,
        )

        benchmark_type = benchmark_cfg.get(
            "type",
            None,
        )

        experiment_name = benchmark_cfg.get(
            "experiment_name",
            None,
        )

        # --------------------------------------------------------------
        # Metrics
        # --------------------------------------------------------------

        metrics = Metrics()

        if benchmark_enabled:

            metrics.csv_path = csv_output_path(
                benchmark_cfg["output_directory"],
                benchmark_type,
                experiment_name,
            )

            metrics.json_path = json_output_path(
                benchmark_cfg["output_directory"],
                benchmark_type,
                experiment_name,
            )

        # --------------------------------------------------------------
        # Visualizer
        # --------------------------------------------------------------

        if benchmark_enabled:

            visualizer = Visualizer(
                output_video=video_output_path(
                    benchmark_cfg["output_directory"],
                    benchmark_type,
                    experiment_name,
                ),
                fps=video_loader.fps,
                frame_width=video_loader.width,
                frame_height=video_loader.height,
            )

        else:

            visualizer = Visualizer()

        # --------------------------------------------------------------
        # Pipeline
        # --------------------------------------------------------------

        pipeline = Pipeline(
            video_loader=video_loader,
            detector=detector,
            tracker=tracker,
            trajectory_manager=trajectory_manager,
            speed_estimator=speed_estimator,
            evaluator=evaluator,
            visualizer=visualizer,
            metrics=metrics,
        )

        return pipeline.run()