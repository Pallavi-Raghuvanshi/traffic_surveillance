# ============================================================================
# track_history.py
#
# Maintains per-track motion history and derives kinematic features
# (velocity, heading, acceleration, stationary duration) that every
# anomaly detector reads instead of recomputing independently.
# ============================================================================

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from core.constants import EPSILON_SPEED
from core.schemas import BoundingBox, Track
from utils.geometry import (
    centroid,
    circular_mean,
    circular_variance,
    vector_between,
    vector_heading,
    vector_magnitude,
)


@dataclass(slots=True)
class TrackSnapshot:
    """
    A single observation of a track at a point in time.
    """

    frame_number: int
    timestamp: float
    bbox: BoundingBox
    centroid: tuple[float, float]


@dataclass(slots=True)
class MotionState:
    """
    Derived kinematic state of a track as of its most recent update.
    """

    track_id: int
    class_id: int
    class_name: str
    bbox: BoundingBox
    centroid: tuple[float, float]
    velocity: tuple[float, float]
    speed: float
    heading: float | None
    acceleration: float
    stationary_seconds: float
    frames_tracked: int


class TrackHistoryManager:
    """
    Maintains a rolling, time-windowed motion history for every active
    track and exposes windowed motion queries used by anomaly detectors.

    This is the single place in the engine that turns raw bounding-box
    sequences into kinematic features. Detectors never touch bounding
    boxes directly for motion purposes; they read `MotionState` and
    query this manager for windowed statistics.
    """

    def __init__(
        self,
        *,
        max_history_seconds: float,
        stationary_speed_threshold: float,
    ) -> None:

        self._max_history_seconds = max_history_seconds

        self._stationary_speed_threshold = stationary_speed_threshold

        self._history: dict[int, deque[TrackSnapshot]] = {}

        self._stationary_since: dict[int, float] = {}

        self._previous_speed: dict[int, float] = {}

        self._latest_state: dict[int, MotionState] = {}

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        frame_number: int,
        timestamp: float,
        tracks: list[Track],
    ) -> dict[int, MotionState]:
        """
        Ingest the current frame's tracks and return the freshly
        computed `MotionState` for every track present this frame.
        """

        active_ids: set[int] = set()

        motion_states: dict[int, MotionState] = {}

        for track in tracks:

            active_ids.add(track.track_id)

            snapshot = TrackSnapshot(

                frame_number=frame_number,

                timestamp=timestamp,

                bbox=track.bbox,

                centroid=centroid(track.bbox),
            )

            history = self._history.setdefault(
                track.track_id,
                deque(),
            )

            history.append(snapshot)

            self._trim(history, timestamp)

            velocity, speed, heading = self._compute_motion(history)

            acceleration = self._compute_acceleration(
                track.track_id,
                speed,
                history,
            )

            stationary_seconds = self._update_stationary(
                track.track_id,
                speed,
                timestamp,
            )

            state = MotionState(

                track_id=track.track_id,

                class_id=track.class_id,

                class_name=track.class_name,

                bbox=track.bbox,

                centroid=snapshot.centroid,

                velocity=velocity,

                speed=speed,

                heading=heading,

                acceleration=acceleration,

                stationary_seconds=stationary_seconds,

                frames_tracked=len(history),
            )

            motion_states[track.track_id] = state

            self._latest_state[track.track_id] = state

            self._previous_speed[track.track_id] = speed

        self._prune_inactive(active_ids)

        return motion_states

    # ------------------------------------------------------------------ #
    # Internal — Motion Computation
    # ------------------------------------------------------------------ #

    def _trim(
        self,
        history: deque[TrackSnapshot],
        timestamp: float,
    ) -> None:

        cutoff = timestamp - self._max_history_seconds

        while len(history) > 2 and history[0].timestamp < cutoff:

            history.popleft()

    @staticmethod
    def _compute_motion(
        history: deque[TrackSnapshot],
    ) -> tuple[tuple[float, float], float, float | None]:

        if len(history) < 2:

            return (0.0, 0.0), 0.0, None

        previous = history[-2]

        current = history[-1]

        dt = current.timestamp - previous.timestamp

        if dt <= 0.0:

            return (0.0, 0.0), 0.0, None

        displacement = vector_between(
            previous.centroid,
            current.centroid,
        )

        velocity = (
            displacement[0] / dt,
            displacement[1] / dt,
        )

        speed = vector_magnitude(velocity)

        heading = vector_heading(velocity)

        return velocity, speed, heading

    def _compute_acceleration(
        self,
        track_id: int,
        speed: float,
        history: deque[TrackSnapshot],
    ) -> float:

        if len(history) < 2:

            return 0.0

        dt = history[-1].timestamp - history[-2].timestamp

        if dt <= 0.0:

            return 0.0

        previous_speed = self._previous_speed.get(
            track_id,
            speed,
        )

        return (speed - previous_speed) / dt

    def _update_stationary(
        self,
        track_id: int,
        speed: float,
        timestamp: float,
    ) -> float:

        if speed >= self._stationary_speed_threshold:

            self._stationary_since.pop(track_id, None)

            return 0.0

        since = self._stationary_since.setdefault(
            track_id,
            timestamp,
        )

        return max(0.0, timestamp - since)

    def _prune_inactive(
        self,
        active_ids: set[int],
    ) -> None:

        for stale_id in list(self._history.keys() - active_ids):

            del self._history[stale_id]

            self._stationary_since.pop(stale_id, None)

            self._previous_speed.pop(stale_id, None)

            self._latest_state.pop(stale_id, None)

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #

    def motion_state(
        self,
        track_id: int,
    ) -> MotionState | None:

        return self._latest_state.get(track_id)

    def snapshots(
        self,
        track_id: int,
    ) -> list[TrackSnapshot]:

        return list(
            self._history.get(track_id, ())
        )

    def window_snapshots(
        self,
        track_id: int,
        window_seconds: float,
    ) -> list[TrackSnapshot]:

        history = self._history.get(track_id)

        if not history:

            return []

        cutoff = history[-1].timestamp - window_seconds

        return [
            snapshot
            for snapshot in history
            if snapshot.timestamp >= cutoff
        ]

    def average_heading(
        self,
        track_id: int,
        window_seconds: float,
    ) -> float | None:

        headings = self._windowed_headings(
            track_id,
            window_seconds,
        )

        return circular_mean(headings)

    def heading_variance(
        self,
        track_id: int,
        window_seconds: float,
    ) -> float:

        headings = self._windowed_headings(
            track_id,
            window_seconds,
        )

        return circular_variance(headings)

    def average_speed(
        self,
        track_id: int,
        window_seconds: float,
    ) -> float:

        speeds = self._windowed_speeds(
            track_id,
            window_seconds,
        )

        if not speeds:

            return 0.0

        return sum(speeds) / len(speeds)

    def max_speed(
        self,
        track_id: int,
        window_seconds: float,
    ) -> float:

        speeds = self._windowed_speeds(
            track_id,
            window_seconds,
        )

        return max(speeds, default=0.0)

    def _windowed_headings(
        self,
        track_id: int,
        window_seconds: float,
    ) -> list[float]:

        window = self.window_snapshots(track_id, window_seconds)

        headings: list[float] = []

        for previous, current in zip(window[:-1], window[1:]):

            dt = current.timestamp - previous.timestamp

            if dt <= 0.0:

                continue

            displacement = vector_between(
                previous.centroid,
                current.centroid,
            )

            if vector_magnitude(displacement) < EPSILON_SPEED:

                continue

            heading = vector_heading(displacement)

            if heading is not None:

                headings.append(heading)

        return headings

    def _windowed_speeds(
        self,
        track_id: int,
        window_seconds: float,
    ) -> list[float]:

        window = self.window_snapshots(track_id, window_seconds)

        speeds: list[float] = []

        for previous, current in zip(window[:-1], window[1:]):

            dt = current.timestamp - previous.timestamp

            if dt <= 0.0:

                continue

            displacement = vector_between(
                previous.centroid,
                current.centroid,
            )

            speeds.append(vector_magnitude(displacement) / dt)

        return speeds

    def is_tracked(
        self,
        track_id: int,
    ) -> bool:

        return track_id in self._history

    def clear(
        self,
    ) -> None:

        self._history.clear()

        self._stationary_since.clear()

        self._previous_speed.clear()

        self._latest_state.clear()
