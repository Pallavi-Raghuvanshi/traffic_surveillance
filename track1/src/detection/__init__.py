# detection/__init__.py
# ============================================================================

from .base_detector import BaseDetector
from .faster_rcnn_detector import FasterRCNNDetector
from .ultralytics_detector import UltralyticsDetector

__all__ = [
    "BaseDetector",
    "UltralyticsDetector",
    "FasterRCNNDetector",
]