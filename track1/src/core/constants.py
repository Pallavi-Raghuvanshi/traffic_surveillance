# constants.py
# Project-wide constant values used across the Traffic Surveillance System.
# ============================================================================

from __future__ import annotations

BBOX_FORMAT_XYXY = "xyxy"

SUPPORTED_VIDEO_FORMATS: tuple[str, ...] = (
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
)

# COCO Dataset Class IDs
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