# ============================================================================
# trajectory_manager.py
# ============================================================================

from __future__ import annotations

from collections import defaultdict
from collections import deque

from core.schemas import BoundingBox
from core.schemas import Track


class TrajectoryManager:
    """
    Maintains recent trajectories for every tracked object.

    The manager stores a fixed-length history of bounding boxes
    indexed by track ID. It is responsible only for trajectory
    management and performs no speed estimation.
    """

    def __init__(
        self,
        max_history: int = 30,
    ) -> None:

        self.max_history = max_history

        self._trajectories: dict[
            int,
            deque[BoundingBox]
        ] = defaultdict(

            lambda: deque(
                maxlen=self.max_history
            )
        )

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        tracks: list[Track],
    ) -> None:

        active_track_ids = set()

        for track in tracks:

            active_track_ids.add(
                track.track_id
            )

            self._trajectories[
                track.track_id
            ].append(
                track.bbox
            )

        inactive_tracks = (

            self._trajectories.keys()
            - active_track_ids

        )

        for track_id in list(
            inactive_tracks
        ):

            del self._trajectories[
                track_id
            ]

    # ------------------------------------------------------------------ #
    # Get
    # ------------------------------------------------------------------ #

    def get(
        self,
        track_id: int,
    ) -> list[BoundingBox]:

        trajectory = self._trajectories.get(
            track_id
        )

        if trajectory is None:

            return []

        return list(
            trajectory
        )

    # ------------------------------------------------------------------ #
    # Contains
    # ------------------------------------------------------------------ #

    def contains(
        self,
        track_id: int,
    ) -> bool:

        return (
            track_id
            in self._trajectories
        )

    # ------------------------------------------------------------------ #
    # Remove
    # ------------------------------------------------------------------ #

    def remove(
        self,
        track_id: int,
    ) -> None:

        self._trajectories.pop(
            track_id,
            None,
        )

    # ------------------------------------------------------------------ #
    # Clear
    # ------------------------------------------------------------------ #

    def clear(
        self,
    ) -> None:

        self._trajectories.clear()

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def num_tracks(
        self,
    ) -> int:

        return len(
            self._trajectories
        )