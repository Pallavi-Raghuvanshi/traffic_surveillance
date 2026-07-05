# schemas.py
# Description:
#     Shared data models used throughout the Traffic Surveillance System.
# ============================================================================

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VideoMetadata:
    """
    Stores immutable metadata of an input video.
    """

    filename: str
    width: int
    height: int
    fps: float
    frame_count: int
    duration: float
    codec: str