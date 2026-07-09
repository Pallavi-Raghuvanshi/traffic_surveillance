# ============================================================================
# benchmark_summary.py
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AnomalyBenchmarkSummary:
    """
    Immutable summary returned by Pipeline.run().

    This object is the single return type exchanged between Pipeline,
    ExperimentRunner, main() and benchmark scripts.
    """

    frames_processed: int

    average_fps: float

    average_processing_time_ms: float

    average_tracks: float

    total_anomalies: int

    anomalies_per_type: dict[str, int] = field(
        default_factory=dict
    )

    anomalies_per_severity: dict[str, int] = field(
        default_factory=dict
    )

    average_confidence: float = 0.0
