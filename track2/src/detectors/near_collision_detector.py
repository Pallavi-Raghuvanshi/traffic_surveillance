# ============================================================================
# near_collision_detector.py
#
# Flags two vehicles that are on a rapid closing trajectory and pass
# within a short, estimated time-to-collision of one another without
# an actual impact being confirmed — a near-miss.
# ============================================================================

from __future__ import annotations

from itertools import combinations

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory

from engine.track_history import MotionState

from utils.geometry import bbox_gap_distance, vector_between, vector_magnitude


@AnomalyDetectorFactory.register("near_collision")
class NearCollisionDetector(BaseAnomalyDetector):
    """
    Detects near-miss encounters between two vehicles using an
    estimated time-to-collision (TTC).
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["near_collision"]

        self._proximity_distance_px = cfg["proximity_distance_px"]

        self._ttc_threshold_seconds = cfg["ttc_threshold_seconds"]

        self._closing_speed_threshold = cfg["closing_speed_threshold"]

        self._min_speed = cfg["min_speed"]

        self._reported: set[frozenset[int]] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.NEAR_COLLISION

    # ------------------------------------------------------------------ #
    # Process
    # ------------------------------------------------------------------ #

    def process(
        self,
        context: FrameContext,
    ) -> list[AnomalyEvent]:

        events: list[AnomalyEvent] = []

        vehicles = [
            track
            for track in context.tracks
            if track.class_name in VEHICLE_CLASS_NAMES
        ]

        for track_a, track_b in combinations(vehicles, 2):

            pair_key = frozenset(
                (track_a.track_id, track_b.track_id)
            )

            state_a = context.motion_states.get(track_a.track_id)

            state_b = context.motion_states.get(track_b.track_id)

            if state_a is None or state_b is None:

                continue

            if (

                state_a.speed < self._min_speed

                and state_b.speed < self._min_speed

            ):

                self._reported.discard(pair_key)

                continue

            gap = bbox_gap_distance(track_a.bbox, track_b.bbox)
            heading = self._heading_difference(
                state_a.heading,
                state_b.heading,
            )

            if heading < 45:
                continue
            if gap > self._proximity_distance_px:

                self._reported.discard(pair_key)

                continue

            ttc = self._time_to_collision(state_a, state_b)

            if ttc is None or ttc > self._ttc_threshold_seconds:

                continue

            if pair_key in self._reported:

                continue

            self._reported.add(pair_key)

            events.append(

                AnomalyEvent(

                    anomaly_type=self.anomaly_type,

                    frame_number=context.frame_number,

                    timestamp=context.timestamp,

                    track_ids=(track_a.track_id, track_b.track_id),

                    confidence=max(

                        0.0,

                        min(1.0, 1.0 - ttc / self._ttc_threshold_seconds),
                    ),

                    severity=self._severity(ttc),

                    description=(
                        f"Vehicles {track_a.track_id} and {track_b.track_id} "
                        f"had a near collision (TTC={ttc:.2f}s)."
                    ),

                    metadata={"ttc_seconds": ttc, "gap_px": gap},
                )
            )

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _heading_difference(
        heading_a: float | None,
        heading_b: float | None,
    ) -> float:

        if heading_a is None or heading_b is None:
            return 180.0

        diff = abs(heading_a - heading_b)

        return min(diff, 360 - diff)
    def _time_to_collision(
        self,
        state_a: MotionState,
        state_b: MotionState,
    ) -> float | None:

        relative_position = vector_between(
            state_b.centroid,
            state_a.centroid,
        )

        distance = vector_magnitude(relative_position)

        if distance < 1e-6:

            return 0.0

        direction = (
            relative_position[0] / distance,
            relative_position[1] / distance,
        )

        relative_velocity = (
            state_a.velocity[0] - state_b.velocity[0],
            state_a.velocity[1] - state_b.velocity[1],
        )

        closing_speed = -(

            relative_velocity[0] * direction[0]

            + relative_velocity[1] * direction[1]
        )

        if closing_speed < self._closing_speed_threshold:

            return None

        return distance / closing_speed

    @staticmethod
    def _severity(
        ttc: float,
    ) -> AnomalySeverity:

        if ttc <= 0.5:

            return AnomalySeverity.CRITICAL

        if ttc <= 1.0:

            return AnomalySeverity.HIGH

        return AnomalySeverity.MEDIUM

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._reported.clear()
