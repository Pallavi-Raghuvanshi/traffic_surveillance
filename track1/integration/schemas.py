from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ReIDResult:

    track_id: int

    vehicle_id: int

    similarity: float

    is_new_vehicle: bool
    frame_number: int