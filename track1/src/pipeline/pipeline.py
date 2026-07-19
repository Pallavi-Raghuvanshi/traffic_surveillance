# ============================================================================
# pipeline.py
# ============================================================================

from __future__ import annotations
import time # for measuring execution time

from core.logger import get_logger

from evaluation.benchmark_summary import BenchmarkSummary
from evaluation.evaluator import Evaluator
from evaluation.metrics import Metrics

logger = get_logger(__name__)

class Pipeline:
    """
    Video load
        ↓
    Detection
        ↓
    Tracking
        ↓
    Trajectory Update
        ↓
    Visualization
        ↓
    Metrics
        ↓
    Evaluation

    Pipeline is intentionally unaware of:

    - benchmarking
    - exporting
    - experiment types
    - output directories
    """

    def __init__(
        self,
        *,
        video_loader,
        detector,
        tracker,
        # trajectory_manager,
        # speed_estimator,
        visualizer,
        metrics: Metrics,
        evaluator: Evaluator,
    ) -> None:

        self.video_loader = video_loader
        self.detector = detector
        self.tracker = tracker
        # self.trajectory_manager = trajectory_manager
        # self.speed_estimator = speed_estimator
        self.visualizer = visualizer
        self.metrics = metrics
        self.evaluator = evaluator

    def run(self) -> BenchmarkSummary:
        logger.info("Pipeline started.")
        for frame_number, frame in self.video_loader:
            
            start_time = time.perf_counter() # time counted from a randome state
            detections = self.detector.detect(frame)
            tracks = self.tracker.update(detections, frame)
            # self.trajectory_manager.update(tracks)
            # speeds: list[float] = []
            # speed_map: dict[int, float] = {}
            # for track in tracks:
            #     trajectory = self.trajectory_manager.get(track.track_id)
            #     speed = self.speed_estimator.estimate(trajectory)
            #     speeds.append(speed)
            #     speed_map[track.track_id] = speed

            # time taken for detection, tracking and trajectory
            processing_time = time.perf_counter() - start_time
            fps = 1.0 / processing_time if processing_time > 0 else 0.0

            annotated_frame = (
                self.visualizer.draw_tracks(
                    frame=frame,
                    tracks=tracks,
                    # speeds=speed_map,
                    fps=fps,
                    frame_number=frame_number,
                )
            )

            # Visualization
            self.visualizer.write(annotated_frame)

            # Runtime Metrics
            self.metrics.update(
                processing_time=processing_time,
                num_detections=len(detections),
                num_tracks=len(tracks),
                # speeds=speeds,
            )

            # Algorithm Evaluation
            self.evaluator.update(
                detections=detections,
                tracks=tracks,
                # speeds=speeds,
            )

        # Cleanup
        self.visualizer.close()
        logger.info("Pipeline finished.")
        return self.metrics.summary()