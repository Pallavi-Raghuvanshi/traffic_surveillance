# ============================================================================
# benchmark_detectors.py
# ============================================================================
"""
Benchmark all configured detectors on the same input video.

Outputs
-------
outputs/
    detector_benchmark/
        detector_name/
            annotated.mp4
            detections.csv
            metrics.json

    detector_results.csv
"""

from __future__ import annotations

import csv
import time
from pathlib import Path

from core.config import Config

from detection import DetectorFactory

from evaluation.detector_metrics import DetectorMetrics

from input import VideoLoader

from visualization.benchmark_visualizer import (
    BenchmarkVisualizer,
)

from utils.file_utils import (
    benchmark_csv_path,
    csv_output_path,
    experiment_directory,
    json_output_path,
    video_output_path,
)


class DetectorBenchmark:
    """
    Benchmarks every detector listed in config.yaml.
    """

    def __init__(
        self,
    ) -> None:

        self.config = Config()

        self.results: list[dict] = []

    def run(
        self,
    ) -> None:

        detectors = self.config[
            "benchmark"
        ][
            "detectors"
        ]

        for detector_cfg in detectors:

            algorithm = detector_cfg["algorithm"]
            model = detector_cfg["model"]

            print("\n" + "=" * 60)
            print(
                f"Benchmarking : {algorithm} ({model})"
            )
            print("=" * 60)

            self.config["detection"][
                "algorithm"
            ] = algorithm

            self.config["detection"][
                "model"
            ] = model

            self._run_detector(
                detector_cfg
            )

        self._save_summary()

        self._print_summary()

    def _run_detector(
        self,
        detector_cfg: dict,
    ) -> None:

        algorithm = detector_cfg[
            "algorithm"
        ]

        detector_name = detector_cfg[
            "model"
        ]

        detector = DetectorFactory.create(
            self.config
        )

        video_loader = VideoLoader(
            self.config["paths"]["video"]
        )

        metrics = DetectorMetrics()

        experiment_name = (
            f"{algorithm}_"
            f"{Path(detector_name).stem}"
        )

        experiment_directory(

            self.config["benchmark"][
                "output_directory"
            ],

            experiment_name,
        )

        visualizer = BenchmarkVisualizer(

            output_video=video_output_path(

                self.config["benchmark"][
                    "output_directory"
                ],

                experiment_name,
            ),

            fps=video_loader.fps,

            frame_width=video_loader.width,

            frame_height=video_loader.height,

            detector_name=experiment_name,
        )

        # ---------------------------------------------------------
        # Benchmark Loop
        # ---------------------------------------------------------

        for frame_number, frame in video_loader:

            start = time.perf_counter()

            detections = detector.detect(
                frame
            )

            inference_time = (
                time.perf_counter()
                - start
            )

            metrics.update(

                frame_number=frame_number,

                inference_time=inference_time,

                detections=detections,
            )

            annotated = visualizer.draw(

                frame=frame,

                detections=detections,

                fps=metrics.average_fps,

                frame_number=frame_number,
            )

            if self.config["benchmark"][
                "save_video"
            ]:

                visualizer.write(
                    annotated
                )

        visualizer.close()

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
            "detector"
        ] = experiment_name

        self.results.append(
            summary
        )

    def _save_summary(
        self,
    ) -> None:
        """
        Save detector benchmark summary.
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

                    "detector",

                    "frames_processed",

                    "average_fps",

                    "average_detections",

                    "average_inference_time_ms",
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
        Print detector benchmark summary.
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
                    "average_detections"
                ],
            ),

            reverse=True,
        )

        print()

        print("=" * 80)

        print(
            "DETECTOR BENCHMARK SUMMARY"
        )

        print("=" * 80)

        print(
            f"{'Detector':<35}"
            f"{'FPS':>10}"
            f"{'Detections':>15}"
            f"{'Inference(ms)':>18}"
        )

        print("-" * 80)

        for result in ranking:

            print(

                f"{result['detector']:<35}"

                f"{result['average_fps']:>10.2f}"

                f"{result['average_detections']:>15.2f}"

                f"{result['average_inference_time_ms']:>18.2f}"

            )

        print("=" * 80)


# ============================================================================
# Entry Point
# ============================================================================

def main() -> None:

    benchmark = DetectorBenchmark()

    benchmark.run()


if __name__ == "__main__":

    main()