# __init__.py

from .config import Config
from .logger import get_logger

from .schemas import (
    VideoMetadata,
    BoundingBox,
    Detection,
    TrackState,
    Track,
)

from .exceptions import (
    TrafficSurveillanceError,
    ConfigurationError,
    VideoError,
    DetectorError,
    TrackerError,
    CalibrationError,
    SpeedEstimationError,
    EvaluationError,
)

from .constants import *