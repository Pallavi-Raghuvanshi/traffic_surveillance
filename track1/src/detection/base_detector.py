# base_detector.py
# Specifies the blueprint for all Detectors which will be its subclass
# ============================================================================

from __future__ import annotations
from abc import abstractmethod, ABC # Abstract Base Class
import numpy as np

from core.schemas import Detection

class BaseDetector(ABC):

    @abstractmethod # forces child classes to implement the method
    def detect(self, frame: np.ndarray) -> list[Detection]:
        """Detect objects in a single image"""

    def reset(self) -> None:
        """Reset detector state or clear the memory regarding previous frames."""