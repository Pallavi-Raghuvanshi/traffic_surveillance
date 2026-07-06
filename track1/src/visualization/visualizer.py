# ============================================================================
# visualizer.py
# ============================================================================

from __future__ import annotations

import cv2
import numpy as np

from core.schemas import Track


class Visualizer:
    """
    Draws detections, tracks and speeds onto video frames.
    """

    def __init__(
        self,
        show_labels: bool = True,
        show_speed: bool = True,
        show_track_id: bool = True,
    ) -> None:

        self.show_labels = show_labels
        self.show_speed = show_speed
        self.show_track_id = show_track_id

    def draw_tracks(
        self,
        frame: np.ndarray,
        tracks: list[Track],
        speeds: dict[int, float],
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

            text = []

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

        return output