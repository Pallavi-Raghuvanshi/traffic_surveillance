# video_loader.py

from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

from core.logger import get_logger

logger = get_logger(__name__)


class VideoLoader:
    """
    Production-ready video loader for Track 1.

    Responsibilities:
    - Open and validate a video
    - Extract metadata
    - Read frames sequentially
    - Random frame access
    - Iterator support
    - Context manager support
    """

    def __init__(self, video_path: str | Path):

        self.video_path = Path(video_path)

        if not self.video_path.exists():
            raise FileNotFoundError(
                f"Video not found: {self.video_path}"
            )

        self.cap = cv2.VideoCapture(str(self.video_path))

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Unable to open video: {self.video_path}"
            )

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self.height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        self.frame_count = int(
            self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        self.duration = (
            self.frame_count / self.fps
            if self.fps > 0
            else 0
        )

        self.current_frame = 0

        logger.info(
            "Loaded video '%s' (%d frames)",
            self.video_path.name,
            self.frame_count,
        )

    def is_opened(self) -> bool:
        return self.cap.isOpened()

    def read(self) -> tuple[bool, np.ndarray | None]:

        success, frame = self.cap.read()

        if success:
            self.current_frame += 1
            return True, frame

        return False, None

    def get_frame(
        self,
        frame_index: int,
    ) -> np.ndarray | None:

        if (
            frame_index < 0
            or frame_index >= self.frame_count
        ):
            raise IndexError(
                "Frame index out of range."
            )

        current = self.current_frame

        self.cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_index,
        )

        success, frame = self.cap.read()

        self.cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            current,
        )

        return frame if success else None

    def reset(self):

        self.cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            0,
        )

        self.current_frame = 0

    def release(self):

        if self.cap.isOpened():
            self.cap.release()

            logger.info(
                "Released video: %s",
                self.video_path.name,
            )

    def __iter__(self) -> Iterator[
        tuple[int, np.ndarray]
    ]:

        self.reset()

        return self

    def __next__(self):

        success, frame = self.read()

        if not success:
            raise StopIteration

        return self.current_frame, frame

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):

        self.release()