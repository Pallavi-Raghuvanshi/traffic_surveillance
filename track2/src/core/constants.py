# constants.py
#
# Description:
#     Project-wide constant values used across the Traffic Anomaly
#     Detection System.
#
# Note:
#     Do NOT store configurable parameters here.
#     Configurable values belong in config.yaml.
# ============================================================================

from __future__ import annotations

# ============================================================================
# Vehicle Classes
# ============================================================================

# Class names considered relevant for anomaly detection. Detections
# belonging to other classes (e.g. "person") are ignored by detectors
# that are vehicle-specific.
VEHICLE_CLASS_NAMES: tuple[str, ...] = (
    "car",
    "bus",
    "truck",
    "motorcycle",
)

# ============================================================================
# Anomaly Detector Registry Keys
# ============================================================================

DETECTOR_COLLISION = "collision"
DETECTOR_NEAR_COLLISION = "near_collision"
DETECTOR_STALLED_VEHICLE = "stalled_vehicle"
DETECTOR_SUDDEN_STOP = "sudden_stop"
DETECTOR_ABNORMAL_TRAJECTORY = "abnormal_trajectory"
DETECTOR_WRONG_WAY = "wrong_way"
DETECTOR_VEHICLE_REVERSAL = "vehicle_reversal"

ALL_DETECTOR_KEYS: tuple[str, ...] = (
    DETECTOR_COLLISION,
    DETECTOR_NEAR_COLLISION,
    DETECTOR_STALLED_VEHICLE,
    DETECTOR_SUDDEN_STOP,
    DETECTOR_ABNORMAL_TRAJECTORY,
    DETECTOR_WRONG_WAY,
    DETECTOR_VEHICLE_REVERSAL,
)

# ============================================================================
# Numerical Safety
# ============================================================================

# Speeds/vectors below this magnitude are treated as numerically zero
# to avoid division-by-zero and heading-angle noise on static tracks.
EPSILON_SPEED = 1e-6

# ============================================================================
# Supported File Extensions
# ============================================================================

SUPPORTED_VIDEO_FORMATS: tuple[str, ...] = (
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
)

SUPPORTED_TRACK_EXPORT_FORMATS: tuple[str, ...] = (
    ".jsonl",
)
