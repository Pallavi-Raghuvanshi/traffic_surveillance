# ============================================================================
# collision_detector.py
#
# Flags two vehicles whose bounding boxes overlap sharply while at
# least one of them was moving at meaningful speed immediately
# beforehand and then decelerated abruptly — the geometric and
# kinematic signature of an impact, inferred purely from track
# geometry and motion history.
# ============================================================================

from __future__ import annotations

from itertools import combinations

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory

from utils.geometry import iou


@AnomalyDetectorFactory.register("collision")
class CollisionDetector(BaseAnomalyDetector):
    """
    Detects vehicle-to-vehicle collisions.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["collision"]

        self._iou_threshold = cfg["iou_threshold"]

        self._pre_impact_min_speed = cfg["pre_impact_min_speed"]

        self._deceleration_ratio = cfg["deceleration_ratio"]

        self._confirmation_window_seconds = cfg["confirmation_window_seconds"]

        self._reported: set[frozenset[int]] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.COLLISION

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

            overlap = iou(track_a.bbox, track_b.bbox)

            if overlap < self._iou_threshold:

                self._reported.discard(pair_key)

                continue

            if pair_key in self._reported:

                continue

            impact_a = self._confirms_impact(context, track_a.track_id)

            impact_b = self._confirms_impact(context, track_b.track_id)

            if not (impact_a or impact_b):

                continue

            self._reported.add(pair_key)

            events.append(

                AnomalyEvent(

                    anomaly_type=self.anomaly_type,

                    frame_number=context.frame_number,

                    timestamp=context.timestamp,

                    track_ids=(track_a.track_id, track_b.track_id),

                    confidence=min(1.0, overlap + 0.3),

                    severity=self._severity(overlap, impact_a, impact_b),

                    description=(
                        f"Vehicles {track_a.track_id} and {track_b.track_id} "
                        f"collided (IoU={overlap:.2f})."
                    ),

                    metadata={
                        "iou": overlap,
                        "impact_a": impact_a,
                        "impact_b": impact_b,
                    },
                )
            )

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _confirms_impact(
        self,
        context: FrameContext,
        track_id: int,
    ) -> bool:

        peak_speed = context.history.max_speed(
            track_id,
            self._confirmation_window_seconds,
        )

        if peak_speed < self._pre_impact_min_speed:

            return False

        state = context.motion_states.get(track_id)

        if state is None:

            return False

        return state.speed <= peak_speed * (1.0 - self._deceleration_ratio)

    @staticmethod
    def _severity(
        overlap: float,
        impact_a: bool,
        impact_b: bool,
    ) -> AnomalySeverity:

        if overlap >= 0.6 and impact_a and impact_b:

            return AnomalySeverity.CRITICAL

        if overlap >= 0.45 or (impact_a and impact_b):

            return AnomalySeverity.HIGH

        return AnomalySeverity.MEDIUM

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._reported.clear()
