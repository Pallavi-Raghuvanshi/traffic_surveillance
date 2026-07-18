# ============================================================================
# benchmark_visualizer.py
# ============================================================================

from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np

from core.schemas import Detection

class BenchmarkVisualizer:
    """
    Visualizer used during detector benchmarking.

    Responsibilities
    ----------------
    • Draw detections
    • Display detector name
    • Display FPS
    • Display frame number
    • Save annotated video
    """

    def __init__(
        self,
        output_video: str | Path,
        fps: float,
        frame_width: int,
        frame_height: int,
        detector_name: str,
    ) -> None:

        self.detector_name = detector_name
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(str(output_video), fourcc, fps, (frame_width, frame_height))

    def draw(
        self,
        frame: np.ndarray,
        detections: list[Detection],
        fps: float,
        frame_number: int,
    ) -> np.ndarray:

        output = frame.copy()

        # ------------------------------------------------------------
        # Bounding Boxes
        # ------------------------------------------------------------

        for detection in detections:

            bbox = detection.bbox

            x1 = int(bbox.x1)
            y1 = int(bbox.y1)
            x2 = int(bbox.x2)
            y2 = int(bbox.y2)

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            label = (
                f"{detection.class_name} "
                f"{detection.confidence:.2f}"
            )

            cv2.putText(
                output,
                label,
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        # ------------------------------------------------------------
        # Overlay Information
        # ------------------------------------------------------------

        cv2.putText(
            output,
            f"Detector : {self.detector_name}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            output,
            f"Frame : {frame_number}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        cv2.putText(
            output,
            f"FPS : {fps:.2f}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        cv2.putText(
            output,
            f"Detections : {len(detections)}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        return output

    def write(self, frame: np.ndarray) -> None:
        self.writer.write(frame)

    def close(self) -> None:
        self.writer.release()