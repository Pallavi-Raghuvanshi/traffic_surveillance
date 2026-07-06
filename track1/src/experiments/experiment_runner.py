# ============================================================================
# experiment_runner.py
# ============================================================================

from __future__ import annotations

from core.config import Config

from detection.detector_factory import DetectorFactory

from tracking.tracker_factory import TrackerFactory

from speed.speed_estimator_factory import (
    SpeedEstimatorFactory,
)
from speed.trajectory import TrajectoryManager

from input.video_loader import VideoLoader

from evaluation import Evaluator

from pipeline import Pipeline


class ExperimentRunner:
    """
    Creates and executes an experiment based on config.yaml.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.config = config

    def run(self) -> None:

        # --------------------------------------------------------------
        # Video
        # --------------------------------------------------------------

        video_loader = VideoLoader(
            self.config["paths"]["video"]
        )

        # --------------------------------------------------------------
        # Detector
        # --------------------------------------------------------------

        detector = DetectorFactory.create(
            self.config
        )

        # --------------------------------------------------------------
        # Tracker
        # --------------------------------------------------------------

        tracker = TrackerFactory.create(
            self.config
        )

        # --------------------------------------------------------------
        # Trajectory Manager
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
        # Evaluator
        # --------------------------------------------------------------

        evaluator = Evaluator()

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
        )

        # --------------------------------------------------------------
        # Execute
        # --------------------------------------------------------------

        pipeline.run()