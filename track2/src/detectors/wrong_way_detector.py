# ============================================================================
# wrong_way_detector.py
#
# Flags a vehicle moving opposite to the dominant traffic flow that
# has been learned automatically from historical trajectories (see
# `engine.flow_model.DominantFlowModel`). No manually defined lane
# directions are used.
# ============================================================================

from __future__ import annotations

import math

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory

from utils.geometry import angle_difference


@AnomalyDetectorFactory.register("wrong_way")
class WrongWayDetector(BaseAnomalyDetector):
    """
    Detects vehicles travelling against the learned dominant flow.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["wrong_way"]

        self._angle_threshold = math.radians(
            cfg["angle_threshold_degrees"]
        )

        self._confirmation_seconds = cfg["confirmation_seconds"]

        self._min_speed = cfg["min_speed"]

        self._violation_since: dict[int, float] = {}

        self._reported: set[int] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.WRONG_WAY

    # ------------------------------------------------------------------ #
    # Process
    # ------------------------------------------------------------------ #

    def process(
        self,
        context: FrameContext,
    ) -> list[AnomalyEvent]:

        events: list[AnomalyEvent] = []

        active_ids: set[int] = set()

        for track in context.tracks:

            if track.class_name not in VEHICLE_CLASS_NAMES:

                continue

            active_ids.add(track.track_id)

            state = context.motion_states.get(track.track_id)

            if (

                state is None

                or state.speed < self._min_speed

                or state.heading is None

            ):

                self._violation_since.pop(track.track_id, None)

                self._reported.discard(track.track_id)

                continue

            dominant_heading = context.flow_model.dominant_heading(
                state.centroid
            )

            if dominant_heading is None:

                continue

            deviation = angle_difference(
                state.heading,
                dominant_heading,
            )

            if deviation < self._angle_threshold:

                self._violation_since.pop(track.track_id, None)

                self._reported.discard(track.track_id)

                continue

            since = self._violation_since.setdefault(
                track.track_id,
                context.timestamp,
            )

            duration = context.timestamp - since

            if duration < self._confirmation_seconds:

                continue

            if track.track_id in self._reported:

                continue

            self._reported.add(track.track_id)

            events.append(

                AnomalyEvent(

                    anomaly_type=self.anomaly_type,

                    frame_number=context.frame_number,

                    timestamp=context.timestamp,

                    track_ids=(track.track_id,),

                    confidence=min(1.0, deviation / math.pi),

                    severity=self._severity(deviation, duration),

                    description=(
                        f"Vehicle {track.track_id} is moving opposite to "
                        f"the learned dominant traffic flow."
                    ),

                    metadata={
                        "deviation_degrees": math.degrees(deviation),
                        "duration_seconds": duration,
                    },
                )
            )

        for stale_id in list(self._violation_since.keys() - active_ids):

            self._violation_since.pop(stale_id, None)

            self._reported.discard(stale_id)

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _severity(
        self,
        deviation: float,
        duration: float,
    ) -> AnomalySeverity:

        if (

            deviation >= math.radians(160)

            and duration >= self._confirmation_seconds * 2

        ):

            return AnomalySeverity.CRITICAL

        if duration >= self._confirmation_seconds * 1.5:

            return AnomalySeverity.HIGH

        return AnomalySeverity.MEDIUM

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._violation_since.clear()

        self._reported.clear()
