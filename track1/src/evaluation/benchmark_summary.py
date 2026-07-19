# benchmark_summary.py
# ============================================================================
# Carries final benchmark results from one component to another
# ============================================================================

from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class BenchmarkSummary:
    frames_processed: int
    average_fps: float
    average_processing_time_ms: float
    average_detections: float
    average_tracks: float
    # average_speed: float