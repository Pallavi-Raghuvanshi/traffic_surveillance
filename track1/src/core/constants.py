# constants.py
#
# Description:
#     Project-wide constant values used across the Traffic Surveillance System.
#
# Note:
#     Do NOT store configurable parameters here.
#     Configurable values belong in config.yaml.
# ============================================================================

from __future__ import annotations

# ============================================================================
# COCO Dataset Class IDs
# ============================================================================

COCO_CLASSES: dict[int, str] = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

# Vehicle classes used by this project
VEHICLE_CLASS_IDS: tuple[int, ...] = (
    2,  # Car
    3,  # Motorcycle
    5,  # Bus
    7,  # Truck
)

# ============================================================================
# Bounding Box Formats
# ============================================================================

BBOX_FORMAT_XYXY = "xyxy"
BBOX_FORMAT_XYWH = "xywh"

# ============================================================================
# Supported File Extensions
# ============================================================================

SUPPORTED_VIDEO_FORMATS: tuple[str, ...] = (
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
)