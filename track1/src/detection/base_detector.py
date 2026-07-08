# ============================================================================
# base_detector.py
# ============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import numpy as np

from core.schemas import Detection


class BaseDetector(ABC):
    """
    Abstract interface for all object detectors.

    Every detector implementation must convert its native
    output into a list of Detection objects.
    """

    @abstractmethod
    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:
        """
        Detect objects in a single image.

        Parameters
        ----------
        frame
            Input image in BGR format.

        Returns
        -------
        list[Detection]
            Standardized detection results.
        """

        raise NotImplementedError

    def reset(
        self,
    ) -> None:
        """
        Reset detector state.

        Most detectors are stateless, so the default
        implementation performs no action.
        """

        return