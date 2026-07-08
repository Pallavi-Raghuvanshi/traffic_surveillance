# ============================================================================
# benchmark_summary.py
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BenchmarkSummary:
    """
    Immutable summary returned by Pipeline.run().

    This object is the single return type exchanged between
    Pipeline, ExperimentRunner, main() and benchmark scripts.
    """

    frames_processed: int

    average_fps: float

    average_processing_time_ms: float

    average_detections: float

    average_tracks: float

    average_speed: float