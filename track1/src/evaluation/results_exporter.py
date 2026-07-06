# ============================================================================
# results_exporter.py
# ============================================================================

from __future__ import annotations

import csv
from pathlib import Path


class ResultsExporter:
    """
    Export experiment results to CSV.
    """

    def __init__(
        self,
        output_file: str,
    ) -> None:

        self.output_file = Path(output_file)

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def export(
        self,
        results: dict,
    ) -> None:

        file_exists = self.output_file.exists()

        with self.output_file.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=results.keys(),
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(results)