# ============================================================================
# base_anomaly_detector.py
# ============================================================================

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.schemas import AnomalyEvent, AnomalyType, Track
from engine.flow_model import DominantFlowModel
from engine.track_history import MotionState, TrackHistoryManager


@dataclass(slots=True)
class FrameContext:
    """
    Everything a detector needs to evaluate a single frame.

    Detectors receive this object and this object only. They never
    receive references to other detectors, to the engine, or to the
    raw video frame.
    """

    frame_number: int
    timestamp: float
    tracks: tuple[Track, ...]
    motion_states: dict[int, MotionState]
    history: TrackHistoryManager
    flow_model: DominantFlowModel


class BaseAnomalyDetector(ABC):
    """
    Abstract interface for all anomaly detectors.

    Every detector is single-purpose: it inspects the current
    `FrameContext` and returns zero or more standardized
    `AnomalyEvent` objects. Detectors must not depend on, reference,
    or coordinate with any other detector — the `AnomalyEngine` is the
    only component aware of the full set of active detectors.
    """

    @property
    @abstractmethod
    def anomaly_type(
        self,
    ) -> AnomalyType:
        """
        The anomaly category this detector raises.
        """

        raise NotImplementedError

    @abstractmethod
    def process(
        self,
        context: FrameContext,
    ) -> list[AnomalyEvent]:
        """
        Evaluate the current frame and return any anomaly events.

        Implementations must be side-effect free with respect to
        `context` and may only mutate their own private state.
        """

        raise NotImplementedError

    def reset(
        self,
    ) -> None:
        """
        Reset detector-internal state between video sequences.

        Most detectors keep only lightweight per-track bookkeeping, so
        the default implementation performs no action.
        """

        return
