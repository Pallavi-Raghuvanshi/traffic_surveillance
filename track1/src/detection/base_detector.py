# base_detector.py

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import numpy as np

from core.schemas import Detection


class BaseDetector(ABC):
    """
    Abstract base class for every object detector.

    Any detector implementation
    (YOLO, FasterRCNN, RT-DETR...)
    must inherit this class.
    """

    @abstractmethod
    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:
        """
        Detect objects from an image.

        Parameters
        ----------
        frame

        Returns
        -------
        List[Detection]
        """

        raise NotImplementedError