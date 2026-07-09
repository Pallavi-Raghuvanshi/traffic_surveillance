# ============================================================================
# anomaly_engine.py
#
# Orchestrates every enabled anomaly detector.
#
# Responsibilities
# ----------------
# - Maintain shared motion context (track history, dominant flow)
# - Invoke each enabled detector with a read-only `FrameContext`
# - Aggregate the events every detector returns
# - Suppress duplicate/ongoing events
# - Assign standardized anomaly ids
#
# No detector is aware of any other detector, and no detector is aware
# of the engine itself — they only ever see a `FrameContext`.
# ============================================================================

from __future__ import annotations

import uuid
from dataclasses import replace

from core.config import Config
from core.logger import get_logger
from core.schemas import AnomalyEvent, Track

import detectors as _detectors  # noqa: F401  (import registers all built-in detectors)
from detectors.base_anomaly_detector import BaseAnomalyDetector, FrameContext
from detectors.factory import AnomalyDetectorFactory

from engine.deduplicator import AnomalyDeduplicator
from engine.flow_model import DominantFlowModel
from engine.track_history import TrackHistoryManager


logger = get_logger(__name__)


class AnomalyEngine:
    """
    Central coordinator for Component 2 (Traffic Anomaly Detection).
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        self._config = config

        history_cfg = config["history"]

        self._history = TrackHistoryManager(

            max_history_seconds=history_cfg["max_history_seconds"],

            stationary_speed_threshold=(
                history_cfg["stationary_speed_threshold"]
            ),
        )

        flow_cfg = config["flow_model"]

        self._flow_model = DominantFlowModel(

            cell_size_px=flow_cfg["cell_size_px"],

            ema_alpha=flow_cfg["ema_alpha"],

            min_samples=flow_cfg["min_samples"],

            min_motion_speed=flow_cfg["min_motion_speed"],
        )

        anomaly_cfg = config["anomaly"]

        self._deduplicator = AnomalyDeduplicator(

            cooldown_seconds=anomaly_cfg["dedup_cooldown_seconds"],
        )

        self._detectors: list[BaseAnomalyDetector] = (

            AnomalyDetectorFactory.create_all(

                anomaly_cfg["detectors"],

                config,
            )
        )

        logger.info(

            "AnomalyEngine initialized with detectors: %s",

            [detector.anomaly_type.value for detector in self._detectors],
        )

    # ------------------------------------------------------------------ #
    # Process
    # ------------------------------------------------------------------ #

    def process(
        self,
        frame_number: int,
        timestamp: float,
        tracks: list[Track],
    ) -> list[AnomalyEvent]:

        motion_states = self._history.update(
            frame_number,
            timestamp,
            tracks,
        )

        self._flow_model.update(motion_states)

        context = FrameContext(

            frame_number=frame_number,

            timestamp=timestamp,

            tracks=tuple(tracks),

            motion_states=motion_states,

            history=self._history,

            flow_model=self._flow_model,
        )

        raw_events: list[AnomalyEvent] = []

        for detector in self._detectors:

            raw_events.extend(
                detector.process(context)
            )

        finalized = [
            self._finalize(event)
            for event in raw_events
        ]

        return self._deduplicator.filter(finalized)

    @staticmethod
    def _finalize(
        event: AnomalyEvent,
    ) -> AnomalyEvent:

        return replace(
            event,
            anomaly_id=uuid.uuid4().hex,
        )

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._history.clear()

        self._flow_model.clear()

        self._deduplicator.clear()

        for detector in self._detectors:

            detector.reset()

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def enabled_detectors(
        self,
    ) -> list[str]:

        return [
            detector.anomaly_type.value
            for detector in self._detectors
        ]
