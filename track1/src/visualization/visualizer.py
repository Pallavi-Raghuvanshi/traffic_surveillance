# ============================================================================
# visualizer.py
# ============================================================================

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from core.schemas import Track


class Visualizer:
    """
    Draws tracking results and optionally writes annotated video.

    The Visualizer owns the VideoWriter.

    Pipeline always calls:

        visualizer.write(frame)

    If no output video is configured, write() becomes a no-op.
    """

    def __init__(
        self,
        *,
        show_labels: bool =True,
        show_speed: bool = True,
        show_track_id: bool = True,
        output_video: str | Path | None = None,
        fps: float | None = None,
        frame_width: int | None = None,
        frame_height: int | None = None,
    ) -> None:

        self.show_labels = show_labels

        self.show_speed = show_speed

        self.show_track_id = show_track_id

        self._writer: cv2.VideoWriter | None = None

        if output_video is None:
            return

        if (
            fps is None
            or frame_width is None
            or frame_height is None
        ):
            raise ValueError(
                "fps, frame_width and frame_height "
                "must be provided when output_video "
                "is specified."
            )

        output_video = Path(output_video)

        output_video.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self._writer = cv2.VideoWriter(
            str(output_video),
            fourcc,
            fps,
            (
                frame_width,
                frame_height,
            ),
        )

    # ------------------------------------------------------------------ #
    # Draw
    # ------------------------------------------------------------------ #

    def draw_tracks(
        self,
        frame: np.ndarray,
        tracks: list[Track],
        speeds: dict[int, float],
        *,
        fps: float | None = None,
        frame_number: int | None = None,
    ) -> np.ndarray:

        output = frame.copy()

        for track in tracks:

            x1 = int(track.bbox.x1)
            y1 = int(track.bbox.y1)
            x2 = int(track.bbox.x2)
            y2 = int(track.bbox.y2)

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            text: list[str] = []

            if self.show_track_id:

                text.append(
                    f"ID {track.track_id}"
                )

            if self.show_labels:

                text.append(
                    track.class_name
                )

            if self.show_speed:

                speed = speeds.get(
                    track.track_id,
                    0.0,
                )

                text.append(
                    f"{speed:.1f} km/h"
                )

            cv2.putText(
                output,
                " | ".join(text),
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        if fps is not None:

            cv2.putText(
                output,
                f"FPS : {fps:.2f}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )

        if frame_number is not None:

            cv2.putText(
                output,
                f"Frame : {frame_number}",
                (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2,
            )

        return output

    # ------------------------------------------------------------------ #
    # Video Writer
    # ------------------------------------------------------------------ #

    def write(
        self,
        frame: np.ndarray,
    ) -> None:
        """
        Always safe to call.

        Performs no operation when a VideoWriter
        has not been configured.
        """

        if self._writer is None:
            return

        self._writer.write(frame)

    # ------------------------------------------------------------------ #
    # Cleanup
    # ------------------------------------------------------------------ #

    def close(
        self,
    ) -> None:

        if self._writer is None:
            return

        self._writer.release()

        self._writer = None