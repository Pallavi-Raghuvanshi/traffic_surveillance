# ============================================================================
# video_loader.py
#
# Responsibilities:
#     - Open and validate video files
#     - Extract and cache video metadata
#     - Provide random frame access keyed by frame index
#
# Component 2 uses this exclusively for optional visualization overlay
# (drawing anomaly events onto the source video). No anomaly detector
# reads frame pixels — only `AnomalyVisualizer` does.
# ============================================================================

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from core.exceptions import VideoError
from core.logger import get_logger
from core.schemas import BoundingBox  # noqa: F401  (re-exported for callers)


logger = get_logger(__name__)


class VideoLoader:
    """
    Minimal, random-access video reader.
    """

    def __init__(
        self,
        video_path: str | Path,
    ) -> None:

        self.video_path = Path(
            video_path
        )

        if not self.video_path.exists():

            raise VideoError(
                f"Video not found: {self.video_path}"
            )

        self._capture = cv2.VideoCapture(
            str(self.video_path)
        )

        if not self._capture.isOpened():

            raise VideoError(
                f"Unable to open video: {self.video_path}"
            )

        self._fps = self._capture.get(
            cv2.CAP_PROP_FPS
        )

        if self._fps <= 0:

            raise VideoError(
                "Unable to determine video FPS."
            )

        self._width = int(
            self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self._height = int(
            self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        self._frame_count = int(
            self._capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        logger.info(

            "Loaded video '%s' | %dx%d | %.2f FPS | %d frames",

            self.video_path.name,

            self._width,

            self._height,

            self._fps,

            self._frame_count,
        )

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def fps(
        self,
    ) -> float:

        return self._fps

    @property
    def width(
        self,
    ) -> int:

        return self._width

    @property
    def height(
        self,
    ) -> int:

        return self._height

    @property
    def frame_count(
        self,
    ) -> int:

        return self._frame_count

    # ------------------------------------------------------------------ #
    # Access
    # ------------------------------------------------------------------ #

    def get_frame(
        self,
        frame_index: int,
    ) -> np.ndarray | None:
        """
        Read a specific 0-indexed frame.
        """

        if frame_index < 0 or frame_index >= self._frame_count:

            return None

        self._capture.set(

            cv2.CAP_PROP_POS_FRAMES,

            frame_index,
        )

        success, frame = self._capture.read()

        if not success:

            logger.warning(
                "Unable to read frame %d.",
                frame_index,
            )

            return None

        return frame

    def release(
        self,
    ) -> None:

        if not self._capture.isOpened():

            return

        self._capture.release()

        logger.info(
            "Released video '%s'.",
            self.video_path.name,
        )

    def __enter__(
        self,
    ) -> "VideoLoader":

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:

        self.release()

    def __del__(
        self,
    ) -> None:

        try:

            self.release()

        except Exception:

            pass
