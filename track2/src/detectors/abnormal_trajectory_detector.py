# ============================================================================
# abnormal_trajectory_detector.py
#
# Flags a vehicle whose recent heading is highly unstable (zig-zag or
# erratic motion), measured as the circular variance of its motion
# headings over a short window.
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory


@AnomalyDetectorFactory.register("abnormal_trajectory")
class AbnormalTrajectoryDetector(BaseAnomalyDetector):
    """
    Detects erratic, zig-zag driving trajectories.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["abnormal_trajectory"]

        self._heading_variance_threshold = cfg["heading_variance_threshold"]

        self._min_history_seconds = cfg["min_history_seconds"]

        self._min_speed = cfg["min_speed"]

        self._reported: set[int] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.ABNORMAL_TRAJECTORY

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

            window = context.history.window_snapshots(
                track.track_id,
                self._min_history_seconds,
            )

            if len(window) < 4:

                continue

            variance = context.history.heading_variance(
                track.track_id,
                self._min_history_seconds,
            )

            if variance < self._heading_variance_threshold:

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

                    confidence=min(1.0, variance),

                    severity=self._severity(variance),

                    description=(
                        f"Vehicle {track.track_id} is following an erratic "
                        f"trajectory (heading variance={variance:.2f})."
                    ),

                    metadata={"heading_variance": variance},
                )
            )

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _severity(
        variance: float,
    ) -> AnomalySeverity:

        if variance >= 0.85:

            return AnomalySeverity.HIGH

        if variance >= 0.65:

            return AnomalySeverity.MEDIUM

        return AnomalySeverity.LOW

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._reported.clear()
