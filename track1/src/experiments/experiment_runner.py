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

from pipeline import Pipeline


class ExperimentRunner:

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.config = config

    def run(self) -> None:

        video_loader = VideoLoader(
            self.config.paths.video
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

        pipeline = Pipeline(

            video_loader,

            detector,

            tracker,

            trajectory_manager,

            speed_estimator,

            evaluator,
        )

        pipeline.run()