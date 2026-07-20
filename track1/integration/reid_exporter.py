from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from integration.schemas import ReIDResult


class ReIDExporter:
    """Exports Track 3 Re-ID results."""

    @staticmethod
    def export(
        results: list[ReIDResult],
        json_path: str | Path,
    ) -> None:

        json_path = Path(json_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)

        with json_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                [asdict(result) for result in results],
                file,
                indent=4,
            )