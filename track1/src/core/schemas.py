# schemas.py

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True, slots=True)
class VideoMetadata:
    filename: str
    width: int
    height: int
    fps: float
    frame_count: int
    duration: float
    codec: str


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
class Detection:
    """
    Standard detection object shared by every detector.

    Every detector MUST return this object.
    """
    bbox: BoundingBox
    confidence: float
    class_id: int
    class_name: str

class TrackState(Enum):
    """
    Possible states of a tracked object.
    """
    ACTIVE = "active"
    LOST = "lost"
    REMOVED = "removed"

@dataclass(frozen=True, slots=True)
class Track(Detection):
    """
    Represents a tracked object across multiple frames.

    A Track extends a Detection by assigning a persistent identity
    that remains the same while the object is visible.
    """
    track_id: int
    state: TrackState = TrackState.ACTIVE
    age: int = 1 # no. of frames the object has been tracked for
    lost_frames: int = 0 # no. of frames the object has been lost for
    history: tuple[BoundingBox, ...] = field( # stores previous bounding boxes of the object
        default_factory=tuple # immutable
    )