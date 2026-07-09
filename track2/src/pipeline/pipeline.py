# ============================================================================
# pipeline.py
# ============================================================================

from __future__ import annotations

import time

from core.logger import get_logger

from engine.anomaly_engine import AnomalyEngine

from evaluation.benchmark_summary import AnomalyBenchmarkSummary
from evaluation.evaluator import AnomalyEvaluator
from evaluation.metrics import Metrics

from input.base_track_source import BaseTrackSource
from input.video_loader import VideoLoader

from visualization.anomaly_visualizer import AnomalyVisualizer


logger = get_logger(__name__)


class Pipeline:
    """
    Executes the complete Track 2 anomaly-detection pipeline.

    Pipeline owns the ONLY per-frame processing loop.

    Responsibilities
    ----------------
    Track Ingestion (from Component 1's output)
        ↓
    Anomaly Engine
        ↓
    Visualization (optional)
        ↓
    Metrics
        ↓
    Evaluation

    Pipeline is intentionally unaware of benchmarking, exporting,
    experiment types, or output directories.
    """

    def __init__(
        self,
        *,
        track_source: BaseTrackSource,
        engine: AnomalyEngine,
        metrics: Metrics,
        evaluator: AnomalyEvaluator,
        visualizer: AnomalyVisualizer,
        video_loader: VideoLoader | None = None,
    ) -> None:

        self.track_source = track_source

        self.engine = engine

        self.metrics = metrics

        self.evaluator = evaluator

        self.visualizer = visualizer

        self.video_loader = video_loader

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(
        self,
    ) -> AnomalyBenchmarkSummary:

        logger.info(
            "Pipeline started."
        )

        for frame_tracks in self.track_source:

            start_time = time.perf_counter()

            tracks = list(frame_tracks.tracks)

            # ----------------------------------------------------------
            # Anomaly Detection
            # ----------------------------------------------------------

            events = self.engine.process(

                frame_tracks.frame_number,

                frame_tracks.timestamp,

                tracks,
            )

            processing_time = (
                time.perf_counter() - start_time
            )

            fps = (
                1.0 / processing_time
                if processing_time > 0
                else 0.0
            )

            # ----------------------------------------------------------
            # Visualization (only when a frame image is available)
            # ----------------------------------------------------------

            frame_image = frame_tracks.frame

            if frame_image is None and self.video_loader is not None:

                frame_image = self.video_loader.get_frame(
                    frame_tracks.frame_number - 1
                )

            if frame_image is not None:

                annotated_frame = self.visualizer.draw(

                    frame_image,

                    tracks,

                    events,

                    timestamp=frame_tracks.timestamp,

                    fps=fps,

                    frame_number=frame_tracks.frame_number,
                )

                self.visualizer.write(annotated_frame)

            # ----------------------------------------------------------
            # Runtime Metrics
            # ----------------------------------------------------------

            self.metrics.update(

                processing_time=processing_time,

                num_tracks=len(tracks),
            )

            # ----------------------------------------------------------
            # Anomaly Evaluation
            # ----------------------------------------------------------

            self.evaluator.update(events)

            for event in events:

                logger.info(

                    "Anomaly detected: %s | tracks=%s | severity=%s | "
                    "frame=%d",

                    event.anomaly_type.value,

                    event.track_ids,

                    event.severity.value,

                    event.frame_number,
                )

        # --------------------------------------------------------------
        # Cleanup
        # --------------------------------------------------------------

        self.visualizer.close()

        self.track_source.close()

        if self.video_loader is not None:

            self.video_loader.release()

        logger.info(
            "Pipeline finished."
        )

        return self.evaluator.summary(self.metrics)
