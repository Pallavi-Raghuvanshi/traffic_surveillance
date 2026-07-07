# video_loader.py
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

from core.schemas import VideoMetadata
from core.logger import get_logger

logger = get_logger(__name__)


class VideoLoader:
    """
    Handles all interaction with video sources.

    Notes
    -----
    This class is the ONLY component in the project that communicates
    directly with OpenCV's VideoCapture object.

    Every downstream module (Detector, Tracker, Speed Estimator, etc.)
    receives frames through this class instead of directly using OpenCV.

    This abstraction keeps the rest of the system independent from the
    underlying video backend.

    Attributes
    ----------
    video_path : Path
        Absolute path to the input video.

    """

    ###########################################################################
    # Constructor
    ###########################################################################

    def __init__(self, video_path: str | Path) -> None:
        """
        Initialize the video loader.

        Parameters
        ----------
        video_path : str | Path
            Path to the input video.

        Raises
        ------
        FileNotFoundError
            If the video file does not exist.

        RuntimeError
            If OpenCV fails to open the video.
        """

        # ------------------------------------------------------------
        # Store video path
        # ------------------------------------------------------------

        self.video_path = Path(video_path)

        if not self.video_path.exists():
            raise FileNotFoundError(
                f"Video not found: {self.video_path}"
            )

        # ------------------------------------------------------------
        # Create OpenCV VideoCapture
        # ------------------------------------------------------------

        self._capture = cv2.VideoCapture(str(self.video_path))

        if not self._capture.isOpened():
            raise RuntimeError(
                f"Unable to open video: {self.video_path}"
            )

        # ------------------------------------------------------------
        # Cache video metadata
        # Metadata never changes, therefore read only once.
        # ------------------------------------------------------------

        self._fps = self._capture.get(
            cv2.CAP_PROP_FPS
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

        self._duration = (
            self._frame_count / self._fps
            if self._fps > 0
            else 0.0
        )

        # ------------------------------------------------------------
        # FOURCC Codec
        # ------------------------------------------------------------

        fourcc = int(
            self._capture.get(
                cv2.CAP_PROP_FOURCC
            )
        )

        self._codec = "".join(
            [
                chr((fourcc >> 8 * i) & 0xFF)
                for i in range(4)
            ]
        )

        # ------------------------------------------------------------
        # Current frame pointer
        # ------------------------------------------------------------

        self._current_frame = 0

        # ------------------------------------------------------------
        # Logging
        # ------------------------------------------------------------

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

    ###########################################################################
    # Read-only Properties
    ###########################################################################

    @property
    def fps(self) -> float:
        """Frames per second."""
        return self._fps

    @property
    def width(self) -> int:
        """Video width in pixels."""
        return self._width

    @property
    def height(self) -> int:
        """Video height in pixels."""
        return self._height

    @property
    def frame_count(self) -> int:
        """Total number of frames."""
        return self._frame_count

    @property
    def duration(self) -> float:
        """Video duration in seconds."""
        return self._duration

    @property
    def codec(self) -> str:
        """Video codec (FOURCC)."""
        return self._codec

    @property
    def current_frame(self) -> int:
        """Current frame index."""
        return self._current_frame

    @property
    def metadata(self) -> VideoMetadata:
        """
        Return immutable video metadata.
        """

        return VideoMetadata(
            filename=self.video_path.name,
            width=self._width,
            height=self._height,
            fps=self._fps,
            frame_count=self._frame_count,
            duration=self._duration,
            codec=self._codec,
        )

    ###########################################################################
    # Public Methods
    ###########################################################################

    def is_opened(self) -> bool:
        """
        Check whether the video is still open.

        Returns
        -------
        bool
            True if the video capture is open.
        """

        return self._capture.isOpened()

    def read(self) -> tuple[bool, np.ndarray | None]:
        """
        Read the next frame from the video.

        Returns
        -------
        tuple
            (success, frame)

            success : bool
                True if frame was read successfully.

            frame : np.ndarray | None
                Image in BGR format.
        """

        success, frame = self._capture.read()

        if success:
            self._current_frame += 1
            return True, frame

        logger.debug("Reached end of video.")

        return False, None

    def get_frame(
        self,
        frame_index: int,
    ) -> np.ndarray | None:
        """
        Read a specific frame without changing the current playback position.

        Parameters
        ----------
        frame_index : int

        Returns
        -------
        np.ndarray | None
        """

        if frame_index < 0 or frame_index >= self._frame_count:
            raise IndexError(
                f"Frame index {frame_index} is out of range."
            )

        # Store current OpenCV position
        current_position = int(
            self._capture.get(cv2.CAP_PROP_POS_FRAMES)
        )

        # Jump to requested frame
        self._capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_index,
        )

        success, frame = self._capture.read()

        # Restore previous playback position
        self._capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            current_position,
        )

        if not success:
            logger.warning(
                "Unable to read frame %d.",
                frame_index,
            )
            return None

        return frame

    def reset(self) -> None:
        """
        Reset playback to the first frame.
        """

        self._capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            0,
        )

        self._current_frame = 0

        logger.debug("Playback reset.")

    def release(self) -> None:
        """
        Release OpenCV resources.

        Safe to call multiple times.
        """

        if self._capture.isOpened():
            self._capture.release()

            logger.info(
                "Released video '%s'.",
                self.video_path.name,
            )

    ###########################################################################
    # Iterator Protocol
    ###########################################################################

    def __iter__(
        self,
    ) -> Iterator[tuple[int, np.ndarray]]:
        """
        Allow:

        for frame_id, frame in video_loader
        """

        self.reset()

        return self

    def __next__(
        self,
    ) -> tuple[int, np.ndarray]:
        """
        Return next frame during iteration.
        """

        success, frame = self.read()

        if not success:
            raise StopIteration

        return self._current_frame, frame

    ###########################################################################
    # Context Manager
    ###########################################################################

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

    ###########################################################################
    # Destructor
    ###########################################################################

    def __del__(self) -> None:
        """
        Final safety net.

        If user forgets to call release(),
        OpenCV resources are still cleaned up.
        """

        try:
            self.release()
        except Exception:
            pass