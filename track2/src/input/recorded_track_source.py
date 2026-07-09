# ============================================================================
# recorded_track_source.py
#
# Reads a JSON-Lines track export produced by Component 1 (see
# `export_tracks.py`) and streams it as `FrameTracks`.
#
# This is the primary, production integration path between Component 1
# and Component 2: the two stages run as separate processes connected
# by a plain-text file contract, so Component 2 never imports a single
# line of Component 1's detector/tracker code.
# ============================================================================

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from core.exceptions import TrackSourceError
from core.logger import get_logger
from core.schemas import BoundingBox, FrameTracks, Track

from input.base_track_source import BaseTrackSource


logger = get_logger(__name__)


class RecordedTrackSource(BaseTrackSource):
    """
    Streams `FrameTracks` from a `.jsonl` track export file.

    Each line of the file is a single JSON object:

        {
            "frame_number": int,
            "timestamp": float,
            "tracks": [
                {
                    "track_id": int,
                    "x1": float, "y1": float, "x2": float, "y2": float,
                    "confidence": float,
                    "class_id": int,
                    "class_name": str
                },
                ...
            ]
        }
    """

    def __init__(
        self,
        path: str | Path,
        *,
        fps: float,
    ) -> None:

        self._path = Path(path)

        if not self._path.exists():

            raise TrackSourceError(
                f"Track export not found: {self._path}"
            )

        if fps <= 0:

            raise TrackSourceError(
                "fps must be greater than zero."
            )

        self._fps = fps

        logger.info(

            "Loaded track export '%s'.",

            self._path.name,
        )

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def fps(
        self,
    ) -> float:

        return self._fps

    # ------------------------------------------------------------------ #
    # Iteration
    # ------------------------------------------------------------------ #

    def __iter__(
        self,
    ) -> Iterator[FrameTracks]:

        with self._path.open(

            "r",

            encoding="utf-8",

        ) as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:

                    continue

                try:

                    record = json.loads(line)

                except json.JSONDecodeError as exc:

                    raise TrackSourceError(

                        f"Malformed JSON on line {line_number} of "
                        f"{self._path}."

                    ) from exc

                yield self._parse_record(record)

    @staticmethod
    def _parse_record(
        record: dict,
    ) -> FrameTracks:

        tracks: list[Track] = []

        for raw_track in record.get("tracks", []):

            tracks.append(

                Track(

                    track_id=int(raw_track["track_id"]),

                    bbox=BoundingBox(

                        x1=float(raw_track["x1"]),

                        y1=float(raw_track["y1"]),

                        x2=float(raw_track["x2"]),

                        y2=float(raw_track["y2"]),
                    ),

                    confidence=float(raw_track["confidence"]),

                    class_id=int(raw_track["class_id"]),

                    class_name=str(raw_track["class_name"]),
                )
            )

        return FrameTracks(

            frame_number=int(record["frame_number"]),

            timestamp=float(record["timestamp"]),

            tracks=tuple(tracks),

            frame=None,
        )
