# ============================================================================
# metrics.py
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FrameMetrics:
    """
    Runtime statistics collected for a single frame.
    """

    processing_time_ms: float

    fps: float

    tracks: int


class Metrics:
    """
    Collects runtime statistics only.

    Responsibilities
    ----------------
    - Per-frame runtime metrics
    - Aggregate runtime statistics

    This class intentionally performs NO exporting and knows nothing
    about anomaly events — see `evaluation.evaluator.AnomalyEvaluator`.
    """

    def __init__(
        self,
    ) -> None:

        self._frames: list[FrameMetrics] = []

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        *,
        processing_time: float,
        num_tracks: int,
    ) -> None:

        fps = (
            1.0 / processing_time
            if processing_time > 0
            else 0.0
        )

        self._frames.append(

            FrameMetrics(

                processing_time_ms=processing_time * 1000,

                fps=fps,

                tracks=num_tracks,
            )
        )

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def frames_processed(
        self,
    ) -> int:

        return len(self._frames)

    @property
    def average_processing_time_ms(
        self,
    ) -> float:

        if not self._frames:

            return 0.0

        return sum(

            frame.processing_time_ms
            for frame in self._frames

        ) / len(self._frames)

    @property
    def average_fps(
        self,
    ) -> float:

        if not self._frames:

            return 0.0

        return sum(

            frame.fps
            for frame in self._frames

        ) / len(self._frames)

    @property
    def average_tracks(
        self,
    ) -> float:

        if not self._frames:

            return 0.0

        return sum(

            frame.tracks
            for frame in self._frames

        ) / len(self._frames)
