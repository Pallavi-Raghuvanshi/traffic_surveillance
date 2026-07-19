# visualizer.py
# ============================================================================
# Visualizer used after Detection & Tracking
# ============================================================================

from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np

from src.core.schemas import Track

class Visualizer:

    def __init__(
        self,
        *, # keyword-only parameters ahead
        show_labels: bool = True,
        # show_speed: bool = True,
        show_track_id: bool = True,
        output_video: str | Path,
        fps: float ,
        frame_width: int,
        frame_height: int,
    ) -> None:

        # self.show_speed = show_speed
        self.show_labels = show_labels
        self.show_track_id = show_track_id 
        output_video.parent.mkdir(parents=True, exist_ok=True)
        output_video = Path(output_video)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self._writer = cv2.VideoWriter(str(output_video), fourcc, fps, (frame_width, frame_height))
        if not self._writer.isOpened():
            raise RuntimeError(f"Unable to create output video: {output_video}")

    def draw_tracks(
        self,
        frame: np.ndarray,
        tracks: list[Track],
        # speeds: dict[int, float],
        *,
        fps: float | None = None,
        frame_number: int | None = None,
    ) -> np.ndarray: # annotated frame

        output = frame.copy()

        for track in tracks:

            bbox = track.bbox

            x1 = int(bbox.x1)
            y1 = int(bbox.y1)
            x2 = int(bbox.x2)
            y2 = int(bbox.y2)

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                2,
            )

            label: list[str] = []
            if self.show_track_id:
                label.append(f"ID {track.track_id}")
            if self.show_labels:
                label.append(track.class_name)

            # if self.show_speed:
            #     label.append(f"{speeds.get(track.track_id, 0.0):.1f} km/h")

            cv2.putText(
                output, 
                " | ".join(label),
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        # ------------------------------------------------------------
        # Overlay Information
        # ------------------------------------------------------------
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
    
    def show(self, frame, window_name: str = "Traffic Surveillance") -> bool:
        cv2.imshow(window_name, frame)
        # Press q to exit
        key = cv2.waitKey(1) & 0xFF
        return key != ord("q")

    def write(self, frame: np.ndarray) -> None:
        self._writer.write(frame)

    def close(self) -> None:
        self._writer.release()