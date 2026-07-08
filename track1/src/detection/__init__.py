# ============================================================================
# detection/__init__.py
# ============================================================================

from .base_detector import (
    BaseDetector,
)

from .faster_rcnn_detector import (
    FasterRCNNDetector,
)

from .rtdetr_detector import (
    RTDETRDetector,
)

from .ultralytics_detector import (
    UltralyticsDetector,
)

__all__ = [

    "BaseDetector",

    "UltralyticsDetector",

    "RTDETRDetector",

    "FasterRCNNDetector",
]