# ============================================================================
# metrics_exporter.py
# ============================================================================

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from core.schemas import AnomalyEvent

from evaluation.benchmark_summary import AnomalyBenchmarkSummary


class MetricsExporter:
    """
    Exports `AnomalyBenchmarkSummary` and `AnomalyEvent` records to
    disk. This class performs no metric calculations of its own.
    """

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def export_summary_csv(
        self,
        summary: AnomalyBenchmarkSummary,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        row = asdict(summary)

        row["anomalies_per_type"] = json.dumps(
            row["anomalies_per_type"]
        )

        row["anomalies_per_severity"] = json.dumps(
            row["anomalies_per_severity"]
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=row.keys(),
            )

            writer.writeheader()

            writer.writerow(row)

    def export_summary_json(
        self,
        summary: AnomalyBenchmarkSummary,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(summary),
                file,
                indent=4,
            )

    def export_summary(
        self,
        summary: AnomalyBenchmarkSummary,
        *,
        csv_path: str | Path | None = None,
        json_path: str | Path | None = None,
    ) -> None:

        if csv_path is not None:

            self.export_summary_csv(summary, csv_path)

        if json_path is not None:

            self.export_summary_json(summary, json_path)

    # ------------------------------------------------------------------ #
    # Events
    # ------------------------------------------------------------------ #

    @staticmethod
    def _event_row(
        event: AnomalyEvent,
    ) -> dict:

        return {

            "anomaly_id": event.anomaly_id,

            "anomaly_type": event.anomaly_type.value,

            "frame_number": event.frame_number,

            "timestamp": event.timestamp,

            "track_ids": ";".join(
                str(track_id) for track_id in event.track_ids
            ),

            "confidence": event.confidence,

            "severity": event.severity.value,

            "description": event.description,

            "metadata": json.dumps(event.metadata),
        }

    def export_events_csv(
        self,
        events: list[AnomalyEvent],
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fieldnames = [

            "anomaly_id",

            "anomaly_type",

            "frame_number",

            "timestamp",

            "track_ids",

            "confidence",

            "severity",

            "description",

            "metadata",
        ]

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for event in events:

                writer.writerow(self._event_row(event))

    def export_events_json(
        self,
        events: list[AnomalyEvent],
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        records = [

            {

                "anomaly_id": event.anomaly_id,

                "anomaly_type": event.anomaly_type.value,

                "frame_number": event.frame_number,

                "timestamp": event.timestamp,

                "track_ids": list(event.track_ids),

                "confidence": event.confidence,

                "severity": event.severity.value,

                "description": event.description,

                "metadata": event.metadata,
            }

            for event in events
        ]

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                records,
                file,
                indent=4,
            )

    def export_events(
        self,
        events: list[AnomalyEvent],
        *,
        csv_path: str | Path | None = None,
        json_path: str | Path | None = None,
    ) -> None:

        if csv_path is not None:

            self.export_events_csv(events, csv_path)

        if json_path is not None:

            self.export_events_json(events, json_path)
