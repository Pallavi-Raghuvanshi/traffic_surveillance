# ============================================================================
# vehicle_database.py
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class VehicleRecord:
    """
    Represents a unique vehicle stored in the Re-ID database.
    """

    vehicle_id: int
    embedding: np.ndarray
    representative_crop: np.ndarray


class VehicleDatabase:
    """
    In-memory database of unique vehicles.

    Each vehicle is stored exactly once with its representative
    embedding and crop.

    Notes
    -----
    This implementation is intentionally simple. It can later be
    replaced by SQLite, FAISS, Milvus, etc. without changing the
    remaining integration code.
    """

    def __init__(self) -> None:

        self._vehicles: dict[int, VehicleRecord] = {}

        self._next_vehicle_id = 1

    @property
    def vehicles(self) -> list[VehicleRecord]:
        """
        Returns all registered vehicles.
        """
        return list(self._vehicles.values())

    def add(
        self,
        embedding: np.ndarray,
        crop: np.ndarray,
    ) -> VehicleRecord:
        """
        Register a new vehicle.
        """

        vehicle = VehicleRecord(
            vehicle_id=self._next_vehicle_id,
            embedding=embedding,
            representative_crop=crop,
        )

        self._vehicles[vehicle.vehicle_id] = vehicle

        self._next_vehicle_id += 1

        return vehicle

    def get(
        self,
        vehicle_id: int,
    ) -> VehicleRecord | None:
        """
        Retrieve a vehicle by its ID.
        """

        return self._vehicles.get(vehicle_id)

    def remove(
        self,
        vehicle_id: int,
    ) -> None:
        """
        Remove a vehicle from the database.
        """

        self._vehicles.pop(vehicle_id, None)

    def clear(self) -> None:
        """
        Remove all vehicles.
        """

        self._vehicles.clear()

        self._next_vehicle_id = 1

    def __len__(self) -> int:

        return len(self._vehicles)

    def __iter__(self):

        return iter(self._vehicles.values())