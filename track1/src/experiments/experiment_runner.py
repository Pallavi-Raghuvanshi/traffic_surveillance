# ============================================================================
# experiment_runner.py
# ============================================================================

from __future__ import annotations

from core.config import Config

from input.video_loader import VideoLoader

from detection.detector_factory import (
    DetectorFactory,
)

from tracking.tracker_factory import (
    TrackerFactory,
)

from speed import (
    SpeedEstimatorFactory,
    TrajectoryManager,
)

from evaluation.benchmark_summary import (
    BenchmarkSummary,
)

from evaluation.metrics import (
    Metrics,
)

from evaluation.metrics_exporter import (
    MetricsExporter,
)

from evaluation.evaluator import (
    Evaluator,
)

from visualization.visualizer import (
    Visualizer,
)

from pipeline import Pipeline

from utils.file_utils import (
    video_output_path,
    csv_output_path,
    json_output_path,
)


class ExperimentRunner:
    """
    Composition Root.

    Responsible for creating every object required by the
    application and wiring dependencies together.
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
    ) -> BenchmarkSummary:

        # --------------------------------------------------------------
        # Input
        # --------------------------------------------------------------

        video_loader = VideoLoader(
            self.config["paths"]["video"]
        )

        # --------------------------------------------------------------
        # Detection
        # --------------------------------------------------------------

        detector = DetectorFactory.create(
            self.config
        )

        # --------------------------------------------------------------
        # Tracking
        # --------------------------------------------------------------

        tracker = TrackerFactory.create(
            self.config
        )

        # --------------------------------------------------------------
        # Trajectory
        # --------------------------------------------------------------

        trajectory_manager = (
            TrajectoryManager()
        )

        # --------------------------------------------------------------
        # Speed Estimator
        # --------------------------------------------------------------

        speed_estimator = (
            SpeedEstimatorFactory.create(
                self.config,
                fps=video_loader.fps,
            )
        )

        # --------------------------------------------------------------
        # Metrics
        # --------------------------------------------------------------

        metrics = Metrics()

        metrics_exporter = (
            MetricsExporter()
        )

        # --------------------------------------------------------------
        # Evaluation
        # --------------------------------------------------------------

        evaluator = Evaluator()

        # --------------------------------------------------------------
        # Benchmark Configuration
        # --------------------------------------------------------------

        benchmark_cfg = (
            self.config["benchmark"]
        )

        benchmark_enabled = (
            benchmark_cfg.get(
                "enabled",
                False,
            )
        )

        benchmark_type = (
            benchmark_cfg.get(
                "type"
            )
        )

        experiment_name = (
            benchmark_cfg.get(
                "experiment_name"
            )
        )

        # --------------------------------------------------------------
        # Visualizer
        # --------------------------------------------------------------

        if benchmark_enabled:

            visualizer = Visualizer(

                output_video=video_output_path(
                    benchmark_cfg[
                        "output_directory"
                    ],
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

            metrics=metrics,

            evaluator=evaluator,

            visualizer=visualizer,
        )

        summary = pipeline.run()

        # --------------------------------------------------------------
        # Export
        # --------------------------------------------------------------

        if benchmark_enabled:

            metrics_exporter.export(

                summary,

                csv_path=csv_output_path(
                    benchmark_cfg[
                        "output_directory"
                    ],
                    benchmark_type,
                    experiment_name,
                ),

                json_path=json_output_path(
                    benchmark_cfg[
                        "output_directory"
                    ],
                    benchmark_type,
                    experiment_name,
                ),
            )

        return summary