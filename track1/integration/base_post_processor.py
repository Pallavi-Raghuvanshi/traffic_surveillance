# ============================================================================
# base_post_processor.py
# ============================================================================

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from src.core.schemas import Track


class BasePostProcessor(ABC):

    @abstractmethod
    def process(
        self,
        frame: np.ndarray,
        frame_number: int,
        tracks: list[Track],
    ) -> None:
        """
        Process one frame after tracking.
        """
        raise NotImplementedError