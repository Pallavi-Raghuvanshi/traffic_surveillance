# ============================================================================
# export_tracks.py
#
# Bridges Component 1 (Track 1) output into Component 2 (Track 2) input.
#
# This script drives Track 1's own detector + tracker (YOLO11n +
# official Ultralytics BoT-SORT by default) end-to-end over a video and
# writes a JSON-Lines track export that `RecordedTrackSource` can
# stream frame by frame.
#
# It runs as an isolated script: it adds ONLY track1/src to
# `sys.path` and imports exclusively from Track 1's namespace. It never
# imports anything from Track 2's own `core` / `engine` / `detectors`
# packages, so the two projects' identically-named top-level packages
# (both have a `core`, for example) never collide inside one process.
# Component 2 proper never imports Track 1 code — it only ever reads
# the JSONL file this script produces.
# ============================================================================

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


def _add_track1_to_path(
    track1_root: Path,
) -> None:

    track1_src = track1_root / "src"

    if not track1_src.exists():

        raise FileNotFoundError(
            f"Track 1 src directory not found: {track1_src}"
        )

    sys.path.insert(0, str(track1_src))


def export_tracks(
    *,
    track1_root: Path,
    video_path: Path,
    output_path: Path,
    detection_model: str,
    confidence: float,
    iou: float,
    device: str,
    classes: list[str],
) -> None:
    """
    Run Track 1's YOLO11n detector + official BoT-SORT tracker over
    `video_path` and write one JSON record per frame to `output_path`.
    """

    _add_track1_to_path(track1_root)

    from core.config import Config as Track1Config
    from detection.ultralytics_detector import UltralyticsDetector
    from input.video_loader import VideoLoader
    from tracking.botsort_tracker import BoTSORTTracker

    config = Track1Config()

    config["detection"]["algorithm"] = "ultralytics"

    config["detection"]["model"] = detection_model

    config["detection"]["confidence"] = confidence

    config["detection"]["iou"] = iou

    config["detection"]["device"] = device

    config["detection"]["classes"] = classes

    detector = UltralyticsDetector(config)

    tracker = BoTSORTTracker(config)

    video_loader = VideoLoader(video_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    frame_count = 0

    start_time = time.perf_counter()

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        for frame_number, frame in video_loader:

            detections = detector.detect(frame)

            tracks = tracker.update(detections, frame)

            record = {

                "frame_number": frame_number,

                "timestamp": (frame_number - 1) / video_loader.fps,

                "tracks": [

                    {

                        "track_id": track.track_id,

                        "x1": track.bbox.x1,

                        "y1": track.bbox.y1,

                        "x2": track.bbox.x2,

                        "y2": track.bbox.y2,

                        "confidence": track.confidence,

                        "class_id": track.class_id,

                        "class_name": track.class_name,
                    }

                    for track in tracks
                ],
            }

            file.write(json.dumps(record) + "\n")

            frame_count += 1

            if frame_count % 200 == 0:

                print(
                    f"  ... exported {frame_count} frames"
                )

    video_loader.release()

    elapsed = time.perf_counter() - start_time

    print(

        f"Exported {frame_count} frames "
        f"({frame_count / elapsed:.2f} fps) to {output_path}"
    )


# ============================================================================
# CLI
# ============================================================================

def _resolve_model_path(
    track1_root: Path,
    model: str,
) -> str:

    model_path = Path(model)

    if model_path.is_absolute():

        return str(model_path)

    return str((track1_root / model_path).resolve())


def main() -> None:

    default_track1_root = (
        Path(__file__).resolve().parents[2] / "track1"
    )

    default_output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "tracks"
        / "sample.jsonl"
    )

    parser = argparse.ArgumentParser(

        description=(
            "Export Track 1 detector + tracker output to a Track 2 "
            "JSONL track feed."
        ),
    )

    parser.add_argument(
        "--track1-root",
        default=str(default_track1_root),
    )

    parser.add_argument(
        "--video",
        default=None,
        help="Overrides the video path (default: track1/data/raw/sample.avi).",
    )

    parser.add_argument(
        "--output",
        default=str(default_output),
    )

    parser.add_argument(
        "--model",
        default="models/yolo11n.pt",
    )

    parser.add_argument(
        "--confidence",
        type=float,
        default=0.25,
    )

    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
    )

    parser.add_argument(
        "--device",
        default="cuda",
    )

    parser.add_argument(
        "--classes",
        nargs="+",
        default=["car", "bus", "truck", "motorcycle"],
    )

    args = parser.parse_args()

    track1_root = Path(args.track1_root).resolve()

    if args.video is not None:

        video_path = Path(args.video).resolve()

    else:

        video_path = (
            track1_root / "data" / "raw" / "sample.avi"
        ).resolve()

    output_path = Path(args.output).resolve()

    export_tracks(

        track1_root=track1_root,

        video_path=video_path,

        output_path=output_path,

        detection_model=_resolve_model_path(
            track1_root,
            args.model,
        ),

        confidence=args.confidence,

        iou=args.iou,

        device=args.device,

        classes=args.classes,
    )


if __name__ == "__main__":

    main()
