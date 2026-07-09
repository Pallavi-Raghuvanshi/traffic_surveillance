# ============================================================================
# stalled_vehicle_detector.py
#
# Flags a vehicle that has remained within a small spatial radius for
# an abnormally long duration — inferred purely from how long its
# speed has stayed below the stationary threshold.
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory

from utils.geometry import euclidean_distance


@AnomalyDetectorFactory.register("stalled_vehicle")
class StalledVehicleDetector(BaseAnomalyDetector):
    """
    Detects vehicles stopped for an abnormally long duration.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["stalled_vehicle"]

        self._movement_radius_px = cfg["movement_radius_px"]

        self._stall_duration_seconds = cfg["stall_duration_seconds"]

        self._reported: set[int] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.STALLED_VEHICLE

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

            if state is None:

                continue

            if state.stationary_seconds < self._stall_duration_seconds:

                self._reported.discard(track.track_id)

                continue

            if track.track_id in self._reported:

                continue

            window = context.history.window_snapshots(
                track.track_id,
                self._stall_duration_seconds,
            )

            if len(window) < 2 or not self._within_radius(window):

                continue

            self._reported.add(track.track_id)

            events.append(

                AnomalyEvent(

                    anomaly_type=self.anomaly_type,

                    frame_number=context.frame_number,

                    timestamp=context.timestamp,

                    track_ids=(track.track_id,),

                    confidence=min(

                        1.0,

                        state.stationary_seconds
                        / (self._stall_duration_seconds * 2),
                    ),

                    severity=self._severity(state.stationary_seconds),

                    description=(
                        f"Vehicle {track.track_id} has been stationary for "
                        f"{state.stationary_seconds:.1f}s."
                    ),

                    metadata={
                        "stationary_seconds": state.stationary_seconds,
                    },
                )
            )

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _within_radius(
        self,
        window,
    ) -> bool:

        origin = window[0].centroid

        return all(

            euclidean_distance(origin, snapshot.centroid)
            <= self._movement_radius_px

            for snapshot in window[1:]
        )

    def _severity(
        self,
        stationary_seconds: float,
    ) -> AnomalySeverity:

        if stationary_seconds >= self._stall_duration_seconds * 3:

            return AnomalySeverity.CRITICAL

        if stationary_seconds >= self._stall_duration_seconds * 2:

            return AnomalySeverity.HIGH

        return AnomalySeverity.MEDIUM

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._reported.clear()
