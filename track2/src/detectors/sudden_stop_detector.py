# ============================================================================
# sudden_stop_detector.py
#
# Flags a vehicle whose speed drops sharply within a short window
# relative to its own recent peak speed — a braking event, independent
# of any interaction with another track.
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.constants import VEHICLE_CLASS_NAMES
from core.schemas import AnomalyEvent, AnomalySeverity, AnomalyType

from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory


@AnomalyDetectorFactory.register("sudden_stop")
class SuddenStopDetector(BaseAnomalyDetector):
    """
    Detects abrupt braking events.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        cfg = config["anomaly"]["sudden_stop"]

        self._min_pre_stop_speed = cfg["min_pre_stop_speed"]

        self._speed_drop_ratio = cfg["speed_drop_ratio"]

        self._window_seconds = cfg["window_seconds"]

        self._reported: set[int] = set()

    @property
    def anomaly_type(
        self,
    ) -> AnomalyType:

        return AnomalyType.SUDDEN_STOP

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

            peak_speed = context.history.max_speed(
                track.track_id,
                self._window_seconds,
            )

            if peak_speed < self._min_pre_stop_speed:

                self._reported.discard(track.track_id)

                continue

            dropped = state.speed <= peak_speed * (
                1.0 - self._speed_drop_ratio
            )

            if not dropped:

                if state.speed >= peak_speed * 0.8:

                    self._reported.discard(track.track_id)

                continue

            if track.track_id in self._reported:

                continue

            self._reported.add(track.track_id)

            drop_ratio = 1.0 - (
                state.speed / peak_speed if peak_speed > 0 else 0.0
            )

            events.append(

                AnomalyEvent(

                    anomaly_type=self.anomaly_type,

                    frame_number=context.frame_number,

                    timestamp=context.timestamp,

                    track_ids=(track.track_id,),

                    confidence=min(1.0, drop_ratio),

                    severity=self._severity(drop_ratio, peak_speed),

                    description=(
                        f"Vehicle {track.track_id} braked sharply "
                        f"({peak_speed:.1f} -> {state.speed:.1f} px/s)."
                    ),

                    metadata={
                        "peak_speed": peak_speed,
                        "current_speed": state.speed,
                        "drop_ratio": drop_ratio,
                    },
                )
            )

        return events

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _severity(
        self,
        drop_ratio: float,
        peak_speed: float,
    ) -> AnomalySeverity:

        if drop_ratio >= 0.9 and peak_speed >= self._min_pre_stop_speed * 1.5:

            return AnomalySeverity.HIGH

        if drop_ratio >= 0.75:

            return AnomalySeverity.MEDIUM

        return AnomalySeverity.LOW

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._reported.clear()
