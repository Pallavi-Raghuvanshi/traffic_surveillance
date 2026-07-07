# ============================================================================
# metrics.py
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass

from evaluation.benchmark_summary import BenchmarkSummary


@dataclass(slots=True)
class FrameMetrics:
    """
    Runtime statistics collected for a single frame.
    """

    processing_time_ms: float

    fps: float

    detections: int

    tracks: int


class Metrics:
    """
    Collects runtime statistics only.

    Responsibilities
    ----------------
    - Per-frame runtime metrics
    - Aggregate runtime statistics
    - Build BenchmarkSummary

    This class intentionally performs NO exporting.
    """

    def __init__(
        self,
    ) -> None:

        self._frames: list[FrameMetrics] = []

        self._speed_values: list[float] = []

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        *,
        processing_time: float,
        num_detections: int,
        num_tracks: int,
        speeds: list[float],
    ) -> None:

        fps = (
            1.0 / processing_time
            if processing_time > 0
            else 0.0
        )

        self._frames.append(

            FrameMetrics(

                processing_time_ms=(
                    processing_time * 1000
                ),

                fps=fps,

                detections=num_detections,

                tracks=num_tracks,
            )
        )

        self._speed_values.extend(
            speeds
        )

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def frames_processed(
        self,
    ) -> int:

        return len(
            self._frames
        )

    @property
    def average_processing_time_ms(
        self,
    ) -> float:

        if not self._frames:
            return 0.0

        return sum(

            frame.processing_time_ms

            for frame in self._frames

        ) / len(
            self._frames
        )

    @property
    def average_fps(
        self,
    ) -> float:

        if not self._frames:
            return 0.0

        return sum(

            frame.fps

            for frame in self._frames

        ) / len(
            self._frames
        )

    @property
    def average_detections(
        self,
    ) -> float:

        if not self._frames:
            return 0.0

        return sum(

            frame.detections

            for frame in self._frames

        ) / len(
            self._frames
        )

    @property
    def average_tracks(
        self,
    ) -> float:

        if not self._frames:
            return 0.0

        return sum(

            frame.tracks

            for frame in self._frames

        ) / len(
            self._frames
        )

    @property
    def average_speed(
        self,
    ) -> float:

        if not self._speed_values:
            return 0.0

        return (

            sum(
                self._speed_values
            )

            / len(
                self._speed_values
            )
        )

    # ------------------------------------------------------------------ #
    # Benchmark Summary
    # ------------------------------------------------------------------ #

    def summary(
        self,
    ) -> BenchmarkSummary:

        return BenchmarkSummary(

            frames_processed=(
                self.frames_processed
            ),

            average_fps=(
                self.average_fps
            ),

            average_processing_time_ms=(
                self.average_processing_time_ms
            ),

            average_detections=(
                self.average_detections
            ),

            average_tracks=(
                self.average_tracks
            ),

            average_speed=(
                self.average_speed
            ),
        )