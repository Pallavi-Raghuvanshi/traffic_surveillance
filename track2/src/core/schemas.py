# ============================================================================
# schemas.py
#
# Standardized data contracts for Component 2 (Traffic Anomaly Detection).
#
# `BoundingBox` and `Track` are intentionally minimal and independent of
# any specific detector or tracker implementation. They describe exactly
# what Component 1 (or any equivalent detection/tracking system) is
# expected to provide, and nothing more.
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """
    Bounding box in XYXY format.
    """

    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True, slots=True)
class Track:
    """
    Generic tracked-object contract consumed by Component 2.

    This is intentionally decoupled from Track 1's internal `Track`
    dataclass. Any detector/tracker pipeline that can populate these
    five fields per frame can drive the anomaly engine.
    """

    track_id: int
    bbox: BoundingBox
    confidence: float
    class_id: int
    class_name: str


@dataclass(slots=True)
class FrameTracks:
    """
    A single frame's worth of Component 1 output.

    `frame` is optional: it is required only for visualization and is
    never read by anomaly detectors, which operate purely on track
    geometry and motion history.
    """

    frame_number: int
    timestamp: float
    tracks: tuple[Track, ...]
    frame: np.ndarray | None = field(
        default=None,
        compare=False,
    )


class AnomalyType(Enum):
    """
    Supported anomaly categories.
    """

    COLLISION = "collision"
    NEAR_COLLISION = "near_collision"
    STALLED_VEHICLE = "stalled_vehicle"
    SUDDEN_STOP = "sudden_stop"
    ABNORMAL_TRAJECTORY = "abnormal_trajectory"
    WRONG_WAY = "wrong_way"
    VEHICLE_REVERSAL = "vehicle_reversal"


class AnomalySeverity(Enum):
    """
    Severity assigned to an anomaly event.

    Ordered from least to most severe. `rank` allows numeric
    comparison without relying on declaration order.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def rank(
        self,
    ) -> int:

        return {

            AnomalySeverity.LOW: 0,

            AnomalySeverity.MEDIUM: 1,

            AnomalySeverity.HIGH: 2,

            AnomalySeverity.CRITICAL: 3,

        }[self]


@dataclass(frozen=True, slots=True)
class AnomalyEvent:
    """
    Standardized anomaly event emitted by the anomaly engine.

    `anomaly_id` is assigned by the engine at aggregation time, not by
    the detector that raises the event; detectors may leave it blank.
    """

    anomaly_type: AnomalyType
    frame_number: int
    timestamp: float
    track_ids: tuple[int, ...]
    confidence: float
    severity: AnomalySeverity
    description: str
    anomaly_id: str = ""
    metadata: dict[str, Any] = field(
        default_factory=dict
    )
