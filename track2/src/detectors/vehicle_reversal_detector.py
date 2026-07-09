# ============================================================================
# vehicle_reversal_detector.py
#
# Flags a vehicle whose current heading has reversed by roughly 180
# degrees relative to its own earlier heading. Unlike wrong-way
# driving, this compares a track only against its own motion history,
# not against the learned dominant flow.
# ============================================================================

from __future__ import annotations

import math

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory

from utils.geometry import angle_difference, circular_mean, vector_between, vector_heading


@AnomalyDetectorFactory.register("vehicle_reversal")
class VehicleReversalDetector(BaseAnomalyDetector):
    """
    Detects vehicles that reverse their direction of travel.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["vehicle_reversal"]

        self._angle_threshold = math.radians(
            cfg["angle_threshold_degrees"]
        )

        self._short_window_seconds = cfg["short_window_seconds"]

        self._long_window_seconds = cfg["long_window_seconds"]

        self._min_speed = cfg["min_speed"]

        self._reported: set[int] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.VEHICLE_REVERSAL

    # ------------------------------------------------------------------ #
    # Process
    # ------------------------------------------------------------------ #

    def process(
        self,
        context: FrameContext,
    ) -> list[AnomalyEvent]:

        events: list[AnomalyEvent] = []

        for track in context.tracks:

            if track.class_name not in VEHICLE_CLASS_NAMES:

                continue

            state = context.motion_states.get(track.track_id)

            if state is None or state.speed < self._min_speed:

                self._reported.discard(track.track_id)

                continue

            recent_heading = context.history.average_heading(
                track.track_id,
                self._short_window_seconds,
            )

            baseline_heading = self._baseline_heading(
                context,
                track.track_id,
            )

            if recent_heading is None or baseline_heading is None:

                continue

            deviation = angle_difference(
                recent_heading,
                baseline_heading,
            )

            if deviation < self._angle_threshold:

                self._reported.discard(track.track_id)

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

                    severity=self._severity(deviation),

                    description=(
                        f"Vehicle {track.track_id} reversed its direction "
                        f"of travel."
                    ),

                    metadata={"deviation_degrees": math.degrees(deviation)},
                )
            )

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _baseline_heading(
        self,
        context: FrameContext,
        track_id: int,
    ) -> float | None:
        """
        Mean heading of the older half of the long window, used as the
        track's own recent-history baseline direction of travel.
        """

        long_window = context.history.window_snapshots(
            track_id,
            self._long_window_seconds,
        )

        cutoff = max(2, len(long_window) // 2)

        older_half = long_window[:cutoff]

        if len(older_half) < 2:

            return None

        headings: list[float] = []

        for previous, current in zip(older_half[:-1], older_half[1:]):

            displacement = vector_between(
                previous.centroid,
                current.centroid,
            )

            heading = vector_heading(displacement)

            if heading is not None:

                headings.append(heading)

        return circular_mean(headings)

    @staticmethod
    def _severity(
        deviation: float,
    ) -> AnomalySeverity:

        if deviation >= math.radians(170):

            return AnomalySeverity.HIGH

        return AnomalySeverity.MEDIUM

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._reported.clear()
