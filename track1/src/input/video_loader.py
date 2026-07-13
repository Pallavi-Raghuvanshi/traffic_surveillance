# ============================================================================
# video_loader.py
#
# Responsibilities:
#     - Open and validate video files
#     - Extract and cache video metadata
#     - Provide sequential and random frame access
#     - Support Python iteration
#     - Manage OpenCV resources safely
# ============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

from core.logger import get_logger
from core.schemas import VideoMetadata


logger = get_logger(__name__)


class VideoLoader:
    """
    Handles all interaction with video sources.

    Notes
    -----
    This class is the ONLY component in the project that communicates
    directly with OpenCV's VideoCapture object.

    Every downstream module receives frames exclusively through this
    class, keeping the remainder of the project independent from the
    underlying video backend.
    """

    # ------------------------------------------------------------------ #
    # Constructor
    # ------------------------------------------------------------------ #

    def __init__(
        self,
        video_path: str | Path,
    ) -> None:

        self.video_path = Path(
            video_path
        )

        if not self.video_path.exists():

            raise FileNotFoundError(
                f"Video not found: {self.video_path}"
            )

        self._capture = cv2.VideoCapture(
            str(self.video_path)
        )

        if not self._capture.isOpened():

            raise RuntimeError(
                f"Unable to open video: {self.video_path}"
            )

        # --------------------------------------------------------------
        # Cache immutable metadata
        # --------------------------------------------------------------

        self._fps = self._capture.get(
            cv2.CAP_PROP_FPS
        )

        if self._fps <= 0:

            raise RuntimeError(
                "Unable to determine video FPS."
            )

        self._width = int(
            self._capture.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        self._height = int(
            self._capture.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        self._frame_count = int(
            self._capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        if self._frame_count <= 0:

            logger.warning(
                "Video reports zero frames."
            )

        self._duration = (

            self._frame_count
            / self._fps
        )

        fourcc = int(
            self._capture.get(
                cv2.CAP_PROP_FOURCC
            )
        )

        self._codec = "".join(

            chr(
                (fourcc >> (8 * i))
                & 0xFF
            )

            for i in range(4)

        ).strip()

        self._current_frame = 0

        logger.info(

            (
                "Loaded video '%s' | "
                "%dx%d | "
                "%.2f FPS | "
                "%d frames | "
                "%.2f sec | "
                "Codec: %s"
            ),

            self.video_path.name,

            self._width,

            self._height,

            self._fps,

            self._frame_count,

            self._duration,

            self._codec,
        )

    # ------------------------------------------------------------------ #
    # Read-only Properties
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

    @property
    def duration(
        self,
    ) -> float:

        return self._duration

    @property
    def codec(
        self,
    ) -> str:

        return self._codec

    @property
    def current_frame(
        self,
    ) -> int:

        return self._current_frame

    @property
    def metadata(
        self,
    ) -> VideoMetadata:

        return VideoMetadata(

            filename=self.video_path.name,

            width=self._width,

            height=self._height,

            fps=self._fps,

            frame_count=self._frame_count,

            duration=self._duration,

            codec=self._codec,
        )
    
    # ------------------------------------------------------------------ #
    # Public Methods
    # ------------------------------------------------------------------ #

    def is_opened(
        self,
    ) -> bool:

        """
        Check whether the underlying VideoCapture
        is still open.
        """

        return self._capture.isOpened()

    def read(
        self,
    ) -> tuple[bool, np.ndarray | None]:

        """
        Read the next frame.

        Returns
        -------
        (success, frame)
        """

        success, frame = self._capture.read()

        if success:

            self._current_frame += 1

            return True, frame

        logger.debug(
            "Reached end of video."
        )

        return False, None

    def get_frame(
        self,
        frame_index: int,
    ) -> np.ndarray | None:

        """
        Read a specific frame without affecting the
        current playback position.
        """

        if (

            frame_index < 0

            or frame_index >= self._frame_count

        ):

            raise IndexError(

                f"Frame index {frame_index} "
                "is out of range."
            )

        current_position = int(

            self._capture.get(
                cv2.CAP_PROP_POS_FRAMES
            )
        )

        self._capture.set(

            cv2.CAP_PROP_POS_FRAMES,

            frame_index,
        )

        success, frame = self._capture.read()

        self._capture.set(

            cv2.CAP_PROP_POS_FRAMES,

            current_position,
        )

        self._current_frame = current_position

        if not success:

            logger.warning(

                "Unable to read frame %d.",

                frame_index,
            )

            return None

        return frame

    def reset(
        self,
    ) -> None:

        """
        Reset playback to the beginning.
        """

        self._capture.set(

            cv2.CAP_PROP_POS_FRAMES,

            0,
        )

        self._current_frame = 0

        logger.debug(
            "Playback reset."
        )

    def release(
        self,
    ) -> None:

        """
        Release OpenCV resources.

        Safe to call multiple times.
        """

        if not self._capture.isOpened():

            return

        self._capture.release()

        logger.info(

            "Released video '%s'.",

            self.video_path.name,
        )
    
    # ------------------------------------------------------------------ #
    # Iterator Protocol
    # ------------------------------------------------------------------ #

    def __iter__(
        self,
    ) -> Iterator[
        tuple[int, np.ndarray]
    ]:

        """
        Enable:

            for frame_number, frame in video_loader:
                ...
        """

        self.reset()

        return self

    def __next__(
        self,
    ) -> tuple[
        int,
        np.ndarray,
    ]:

        """
        Return the next frame during iteration.
        """

        success, frame = self.read()

        if not success:

            raise StopIteration

        return (
            self._current_frame,
            frame,
        )

    # ------------------------------------------------------------------ #
    # Context Manager
    # ------------------------------------------------------------------ #

    def __enter__(
        self,
    ) -> "VideoLoader":

        """
        Enter context manager.
        """

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:

        """
        Always release resources.
        """

        self.release()

    # ------------------------------------------------------------------ #
    # Destructor
    # ------------------------------------------------------------------ #

    def __del__(
        self,
    ) -> None:

        """
        Final safety net.

        Ensures VideoCapture resources are released even if
        release() was not explicitly called.
        """

        try:

            self.release()

        except Exception:

            # Never allow exceptions to escape
            # during interpreter shutdown.
            pass