# ============================================================================
# video_writer.py
#
# Thin H.264/MP4 encoder wrapper around PyAV.
#
# OpenCV's bundled FFmpeg plugin has no H.264 encoder available in this
# environment (the `openh264` DLL it needs is not installed), so real
# H.264 encoding is done via PyAV, which statically bundles `libx264`.
# This keeps annotated output videos small (H.264) while remaining
# broadly compatible, with no external DLL or codec-pack dependency.
# ============================================================================

from __future__ import annotations

from pathlib import Path

import av
import numpy as np


class Mp4VideoWriter:
    """
    Encodes BGR frames (as produced by OpenCV) to an H.264 MP4 file.
    """

    def __init__(
        self,
        output_path: str | Path,
        *,
        fps: float,
        frame_width: int,
        frame_height: int,
        crf: int = 23,
        preset: str = "medium",
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._container = av.open(
            str(output_path),
            mode="w",
        )

        self._stream = self._container.add_stream(
            "libx264",
            rate=round(fps),
        )

        self._stream.width = frame_width

        self._stream.height = frame_height

        # yuv420p is required for playback compatibility with most
        # players/browsers; libx264 defaults to a wider color format
        # otherwise.
        self._stream.pix_fmt = "yuv420p"

        self._stream.options = {
            "crf": str(crf),
            "preset": preset,
        }

    # ------------------------------------------------------------------ #
    # Write
    # ------------------------------------------------------------------ #

    def write(
        self,
        frame_bgr: np.ndarray,
    ) -> None:

        video_frame = av.VideoFrame.from_ndarray(
            frame_bgr,
            format="bgr24",
        )

        for packet in self._stream.encode(video_frame):

            self._container.mux(packet)

    # ------------------------------------------------------------------ #
    # Close
    # ------------------------------------------------------------------ #

    def close(
        self,
    ) -> None:

        # Flush any frames buffered inside the encoder.
        for packet in self._stream.encode():

            self._container.mux(packet)

        self._container.close()
