# ============================================================================
# benchmark_trackers.py
# ============================================================================
"""
Benchmark all configured trackers using a fixed detector.

Outputs
-------
outputs/

    tracker_benchmark/

        tracker_name/

            annotated.mp4

            metrics.json

            tracks.csv

    tracker_results.csv
"""

from __future__ import annotations

import csv
import time
from pathlib import Path

from core.config import Config

from detection import DetectorFactory

from tracking import TrackerFactory

from evaluation.metrics import (
    Metrics,
)

from input import VideoLoader

from visualization.visualizer import (
    Visualizer,
)

from utils.file_utils import (
    benchmark_csv_path,
    csv_output_path,
    experiment_directory,
    json_output_path,
    video_output_path,
)


class TrackerBenchmark:
    """
    Benchmarks every tracker listed in config.yaml.
    """

    def __init__(
        self,
    ) -> None:

        self.config = Config()

        self.results: list[dict] = []

    def run(
        self,
    ) -> None:

        detector_cfg = self.config[
            "benchmark"
        ][
            "detectors"
        ]

        self.config["detection"][
            "algorithm"
        ] = detector_cfg[
            "algorithm"
        ]

        self.config["detection"][
            "model"
        ] = detector_cfg[
            "model"
        ]

        trackers = self.config[
            "benchmark"
        ][
            "trackers"
        ]

        for tracker_name in trackers:

            print(
                "\n"
                + "=" * 60
            )

            print(
                f"Benchmarking : {tracker_name}"
            )

            print(
                "=" * 60
            )

            self.config["tracking"][
                "algorithm"
            ] = tracker_name

            self._run_tracker(
                tracker_name
            )

        self._save_summary()

        self._print_summary()

    def _run_tracker(
        self,
        tracker_name: str,
    ) -> None:

        detector = DetectorFactory.create(
            self.config
        )

        tracker = TrackerFactory.create(
            self.config
        )

        video_loader = VideoLoader(
            self.config["paths"]["video"]
        )

        metrics = Metrics()

        experiment_name = tracker_name

        experiment_directory(

            self.config["benchmark"][
                "output_directory"
            ],

            experiment_name,
        )

        visualizer = Visualizer()

        # ---------------------------------------------------------
        # Benchmark Loop
        # ---------------------------------------------------------

        for frame_number, frame in video_loader:

            start = time.perf_counter()

            detections = detector.detect(
                frame
            )

            tracks = tracker.update(

                detections,

                frame,
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            metrics.update(

                frame_number=frame_number,

                processing_time=elapsed,

                tracks=tracks,
            )

            aspeed_map = {
                track.track_id: 0.0
                for track in tracks
            }

            annotated = visualizer.draw_tracks(
                frame=frame,
                tracks=tracks,
                speeds=speed_map,
            )           

        if self.config["benchmark"][
            "save_csv"
        ]:

            metrics.save_csv(

                csv_output_path(

                    self.config["benchmark"][
                        "output_directory"
                    ],

                    experiment_name,
                )
            )

        if self.config["benchmark"][
            "save_json"
        ]:

            metrics.save_json(

                json_output_path(

                    self.config["benchmark"][
                        "output_directory"
                    ],

                    experiment_name,
                )
            )

        summary = metrics.summary()

        summary[
            "tracker"
        ] = experiment_name

        self.results.append(
            summary
        )
    
    def _save_summary(
        self,
    ) -> None:
        """
        Save tracker benchmark summary.
        """

        output_file = benchmark_csv_path(

            self.config["benchmark"][
                "output_directory"
            ]
        )

        with output_file.open(
            "w",
            newline="",
        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=[

                    "tracker",

                    "frames_processed",

                    "average_fps",

                    "average_tracks",

                    "average_processing_time_ms",
                ],
            )

            writer.writeheader()

            writer.writerows(
                self.results
            )

    def _print_summary(
        self,
    ) -> None:
        """
        Print tracker benchmark summary.
        """

        if not self.results:

            print(
                "\nNo benchmark results."
            )

            return

        ranking = sorted(

            self.results,

            key=lambda result: (

                result[
                    "average_fps"
                ],

                result[
                    "average_tracks"
                ],
            ),

            reverse=True,
        )

        print()

        print("=" * 80)

        print(
            "TRACKER BENCHMARK SUMMARY"
        )

        print("=" * 80)

        print(
            f"{'Tracker':<25}"
            f"{'FPS':>10}"
            f"{'Tracks':>15}"
            f"{'Processing(ms)':>20}"
        )

        print("-" * 80)

        for result in ranking:

            print(

                f"{result['tracker']:<25}"

                f"{result['average_fps']:>10.2f}"

                f"{result['average_tracks']:>15.2f}"

                f"{result['average_processing_time_ms']:>20.2f}"

            )

        print("=" * 80)

# ============================================================================
# Entry Point
# ============================================================================

def main() -> None:

    benchmark = TrackerBenchmark()

    benchmark.run()


if __name__ == "__main__":

    main()