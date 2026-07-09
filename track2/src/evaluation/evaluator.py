# ============================================================================
# evaluator.py
# ============================================================================

from __future__ import annotations

from collections import Counter
from statistics import mean

from core.schemas import AnomalyEvent

from evaluation.benchmark_summary import AnomalyBenchmarkSummary
from evaluation.metrics import Metrics


class AnomalyEvaluator:
    """
    Evaluates anomaly-detection output.

    Responsibilities
    ----------------
    - Collect every emitted `AnomalyEvent`
    - Per-type and per-severity anomaly counts
    - Average detection confidence

    Runtime statistics such as FPS and processing time are collected
    exclusively by `Metrics`.
    """

    def __init__(
        self,
    ) -> None:

        self._events: list[AnomalyEvent] = []

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        events: list[AnomalyEvent],
    ) -> None:

        self._events.extend(events)

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def events(
        self,
    ) -> list[AnomalyEvent]:

        return list(self._events)

    @property
    def total_anomalies(
        self,
    ) -> int:

        return len(self._events)

    @property
    def anomalies_per_type(
        self,
    ) -> dict[str, int]:

        counts = Counter(

            event.anomaly_type.value
            for event in self._events
        )

        return dict(counts)

    @property
    def anomalies_per_severity(
        self,
    ) -> dict[str, int]:

        counts = Counter(

            event.severity.value
            for event in self._events
        )

        return dict(counts)

    @property
    def average_confidence(
        self,
    ) -> float:

        if not self._events:

            return 0.0

        return mean(
            event.confidence
            for event in self._events
        )

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def summary(
        self,
        metrics: Metrics,
    ) -> AnomalyBenchmarkSummary:

        return AnomalyBenchmarkSummary(

            frames_processed=metrics.frames_processed,

            average_fps=metrics.average_fps,

            average_processing_time_ms=(
                metrics.average_processing_time_ms
            ),

            average_tracks=metrics.average_tracks,

            total_anomalies=self.total_anomalies,

            anomalies_per_type=self.anomalies_per_type,

            anomalies_per_severity=self.anomalies_per_severity,

            average_confidence=self.average_confidence,
        )

    # ------------------------------------------------------------------ #
    # Console
    # ------------------------------------------------------------------ #

    def print_summary(
        self,
        summary: AnomalyBenchmarkSummary,
    ) -> None:

        print()

        print("=" * 60)

        print("Anomaly Detection Summary")

        print("=" * 60)

        print(
            f"Frames Processed        : {summary.frames_processed}"
        )

        print(
            f"Average FPS             : {summary.average_fps:.2f}"
        )

        print(
            f"Average Processing Time : "
            f"{summary.average_processing_time_ms:.2f} ms"
        )

        print(
            f"Average Tracks          : {summary.average_tracks:.2f}"
        )

        print(
            f"Total Anomalies         : {summary.total_anomalies}"
        )

        print(
            f"Average Confidence      : {summary.average_confidence:.2f}"
        )

        print("-" * 60)

        print("By Type:")

        for anomaly_type, count in sorted(
            summary.anomalies_per_type.items()
        ):

            print(f"  {anomaly_type:<24}: {count}")

        print("By Severity:")

        for severity, count in sorted(
            summary.anomalies_per_severity.items()
        ):

            print(f"  {severity:<24}: {count}")

        print("=" * 60)
