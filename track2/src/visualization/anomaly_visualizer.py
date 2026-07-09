# ============================================================================
# anomaly_visualizer.py
# ============================================================================

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from core.schemas import AnomalyEvent, Track

from visualization.video_writer import Mp4VideoWriter


_TRACK_COLOR = (0, 255, 0)

_ANOMALY_COLOR = (0, 0, 255)

_TEXT_COLOR = (0, 255, 255)


class AnomalyVisualizer:
    """
    Draws tracks and anomaly highlights, and optionally writes an
    annotated output video.

    A track that triggered an anomaly remains highlighted for
    `highlight_seconds` after the event fires, so that single-frame
    events remain visible to a human reviewer rather than flashing for
    one frame only.
    """

    def __init__(
        self,
        *,
        highlight_seconds: float = 2.0,
        output_video: str | Path | None = None,
        fps: float | None = None,
        frame_width: int | None = None,
        frame_height: int | None = None,
        video_crf: int = 23,
        video_preset: str = "medium",
    ) -> None:

        self._highlight_seconds = highlight_seconds

        self._active_highlights: dict[int, tuple[str, str, float]] = {}

        self._writer: Mp4VideoWriter | None = None

        if output_video is None:

            return

        if fps is None or frame_width is None or frame_height is None:

            raise ValueError(

                "fps, frame_width and frame_height must be specified "
                "when output_video is enabled."
            )

        self._writer = Mp4VideoWriter(

            output_video,

            fps=fps,

            frame_width=frame_width,

            frame_height=frame_height,

            crf=video_crf,

            preset=video_preset,
        )

    # ------------------------------------------------------------------ #
    # Draw
    # ------------------------------------------------------------------ #

    def draw(
        self,
        frame: np.ndarray,
        tracks: list[Track],
        events: list[AnomalyEvent],
        *,
        timestamp: float,
        fps: float | None = None,
        frame_number: int | None = None,
    ) -> np.ndarray:

        self._update_highlights(events, timestamp)

        output = frame.copy()

        for track in tracks:

            self._draw_track(output, track, timestamp)

        if fps is not None:

            cv2.putText(
                output,
                f"FPS : {fps:.2f}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                _TEXT_COLOR,
                2,
            )

        if frame_number is not None:

            cv2.putText(
                output,
                f"Frame : {frame_number}",
                (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                _TEXT_COLOR,
                2,
            )

        active_count = len(self._active_highlights)

        cv2.putText(
            output,
            f"Active Anomalies : {active_count}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            _ANOMALY_COLOR,
            2,
        )

        return output

    def _draw_track(
        self,
        output: np.ndarray,
        track: Track,
        timestamp: float,
    ) -> None:

        bbox = track.bbox

        x1, y1, x2, y2 = (
            int(bbox.x1),
            int(bbox.y1),
            int(bbox.x2),
            int(bbox.y2),
        )

        highlight = self._active_highlights.get(track.track_id)

        is_anomalous = (

            highlight is not None

            and timestamp <= highlight[2]
        )

        color = _ANOMALY_COLOR if is_anomalous else _TRACK_COLOR

        thickness = 3 if is_anomalous else 2

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            color,
            thickness,
        )

        label = f"ID {track.track_id} | {track.class_name}"

        if is_anomalous:

            label += f" | {highlight[0]} ({highlight[1]})"

        cv2.putText(
            output,
            label,
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
        )

    def _update_highlights(
        self,
        events: list[AnomalyEvent],
        timestamp: float,
    ) -> None:

        for event in events:

            expiry = event.timestamp + self._highlight_seconds

            for track_id in event.track_ids:

                self._active_highlights[track_id] = (

                    event.anomaly_type.value,

                    event.severity.value,

                    expiry,
                )

        expired = [

            track_id
            for track_id, (_, _, expiry) in self._active_highlights.items()
            if timestamp > expiry
        ]

        for track_id in expired:

            del self._active_highlights[track_id]

    # ------------------------------------------------------------------ #
    # Video Writer
    # ------------------------------------------------------------------ #

    def write(
        self,
        frame: np.ndarray,
    ) -> None:

        if self._writer is None:

            return

        self._writer.write(frame)

    def close(
        self,
    ) -> None:

        if self._writer is None:

            return

        self._writer.close()

        self._writer = None
