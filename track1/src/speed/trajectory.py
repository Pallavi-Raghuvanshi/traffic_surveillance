# ============================================================================
# trajectory.py
# ============================================================================
# maintains history of bounding boxes for each tracked vehicle

from __future__ import annotations

from collections import defaultdict, deque

from core.schemas import BoundingBox
from core.schemas import Track


class TrajectoryManager:
    """
    Maintains the recent trajectory of every tracked vehicle.

    The trajectory is represented as an ordered sequence of
    bounding boxes for each active track.

    This history is later used by the speed estimator.
    """

    def __init__(
        self,
        history_size: int = 30,
    ) -> None:

        self._history_size = history_size

        self._trajectories: dict[
            int,
            deque[BoundingBox],
        ] = defaultdict(
            lambda: deque(maxlen=history_size)
        )

    def update(
        self,
        tracks: list[Track],
    ) -> None:
        """
        Update trajectories using the latest tracker output.
        """

        for track in tracks:

            self._trajectories[
                track.track_id
            ].append(
                track.bbox
            )

    def get(
        self,
        track_id: int,
    ) -> list[BoundingBox]:
        """
        Return trajectory of a vehicle.
        """

        return list(
            self._trajectories.get(
                track_id,
                [],
            )
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all stored trajectories.
        """

        self._trajectories.clear()

    def remove(
        self,
        track_id: int,
    ) -> None:
        """
        Remove a completed trajectory.
        """

        self._trajectories.pop(
            track_id,
            None,
        )

    @property
    def active_tracks(
        self,
    ) -> list[int]:
        """
        Return active track ids.
        """

        return list(
            self._trajectories.keys()
        )