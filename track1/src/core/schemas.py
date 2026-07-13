# schemas.py
# ============================================================================

from dataclasses import dataclass, field
from enum import Enum # used when variable can take only a fixed number of values

@dataclass(frozen=True, slots=True)
class VideoMetadata:
    filename: str
    width: int
    height: int
    fps: float
    frame_count: int
    duration: float
    codec: str

@dataclass(frozen=True, slots=True) # frozen=True -> objects become immutable, slots=True -> fixed memory allocated for object
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

@dataclass(frozen=True, slots=True)
class Detection:
    bbox: BoundingBox
    confidence: float
    class_id: int
    class_name: str

# Possible states of a tracked object
class TrackState(Enum):
    ACTIVE = "active"
    LOST = "lost"
    REMOVED = "removed"

@dataclass(frozen=True, slots=True)
class Track(Detection):
    track_id: int
    state: TrackState = TrackState.ACTIVE
    age: int = 1 # no. of frames the object has been tracked for
    lost_frames: int = 0 # no. of frames the object has been lost for
    history: tuple[BoundingBox, ...] = field(default_factory=tuple) # stores previous bounding boxes of the object & is immutable