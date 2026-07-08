# ============================================================================
# metrics_exporter.py
# ============================================================================

from __future__ import annotations

from dataclasses import asdict
import csv
import json
from pathlib import Path

from evaluation.benchmark_summary import (
    BenchmarkSummary,
)


class MetricsExporter:
    """
    Exports BenchmarkSummary to disk.

    Responsibilities
    ----------------
    - Export CSV
    - Export JSON

    This class performs no metric calculations.
    """

    def export_csv(
        self,
        summary: BenchmarkSummary,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=asdict(
                    summary
                ).keys(),
            )

            writer.writeheader()

            writer.writerow(
                asdict(summary)
            )

    def export_json(
        self,
        summary: BenchmarkSummary,
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

    def export(
        self,
        summary: BenchmarkSummary,
        *,
        csv_path: str | Path | None = None,
        json_path: str | Path | None = None,
    ) -> None:
        """
        Convenience method for exporting one or both formats.
        """

        if csv_path is not None:

            self.export_csv(
                summary,
                csv_path,
            )

        if json_path is not None:

            self.export_json(
                summary,
                json_path,
            )