# schemas.py

from dataclasses import dataclass


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