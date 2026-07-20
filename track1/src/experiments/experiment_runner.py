# experiment_runner.py
# ============================================================================

from __future__ import annotations
from src.core.config import Config

from src.input.video_loader import VideoLoader

from src.detection.ultralytics_detector import UltralyticsDetector
from src.detection.faster_rcnn_detector import FasterRCNNDetector

from src.tracking.bytetrack_tracker import ByteTrackTracker
from src.tracking.deepsort_tracker import DeepSORTTracker
from src.tracking.botsort_tracker import BoTSORTTracker

# from speed import TrajectoryManager
# from speed.pixel_speed_estimator import PixelSpeedEstimator
# from speed.homography_speed_estimator import HomographySpeedEstimator
# from speed.optical_flow_speed_estimator import OpticalFlowSpeedEstimator
# from speed.hybrid_speed_estimator import HybridSpeedEstimator

# from calibration.homography import Homography

from src.evaluation.benchmark_summary import BenchmarkSummary
from src.evaluation.metrics import Metrics
from src.evaluation.metrics_exporter import MetricsExporter
from src.evaluation.evaluator import Evaluator
from src.visualization.visualizer import Visualizer
from src.pipeline import Pipeline
from src.utils.file_utils import video_output_path, csv_output_path, json_output_path

from integration.track1_adapter import Track1Adapter
from integration.vehicle_database import VehicleDatabase
from integration.reid_manager import ReIDManager
from integration.reid_post_processor import ReIDPostProcessor
from integration.reid_exporter import ReIDExporter
from integration.gallery_exporter import GalleryExporter
from track3.demo.predictor import VehicleReIDPredictor
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

checkpoint_path = PROJECT_ROOT / "track3" / "checkpoints" / "best_model.pth"


class ExperimentRunner:

    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> BenchmarkSummary:

        # Input
        video_loader = VideoLoader(self.config["paths"]["video"])

        # Detection
        algorithm = self.config["detection"]["algorithm"].strip().lower()
        if algorithm == "ultralytics":  # YOLO / RT-DETR
            detector = UltralyticsDetector(self.config)
        elif algorithm == "faster_rcnn":  # Faster R-CNN
            detector = FasterRCNNDetector(self.config)
        else:
            raise ValueError(f"Unsupported detector: {algorithm}")

        # Tracking
        algorithm = self.config["tracking"]["algorithm"].strip().lower()
        if algorithm == "bytetrack":
            tracker = ByteTrackTracker(self.config)
        elif algorithm == "deepsort":
            tracker = DeepSORTTracker(self.config)
        elif algorithm == "botsort":
            tracker = BoTSORTTracker(self.config)
        else:
            raise ValueError(f"Unsupported tracker: {algorithm}")

        # Trajectory
        # trajectory_manager = (TrajectoryManager())

        # # Speed Estimator
        # algorithm = self.config["speed"]["algorithm"].strip().lower()

        # if algorithm == "pixel":
        #     speed_estimator = (PixelSpeedEstimator(fps=video_loader.fps))

        # elif algorithm == "homography":
        #     homography = Homography.load(self.config["paths"]["homography"])
        #     speed_estimator = (HomographySpeedEstimator(homography=homography.matrix, fps=video_loader.fps))

        # elif algorithm == "optical_flow":
        #     speed_estimator = (OpticalFlowSpeedEstimator(self.config))

        # elif algorithm == "hybrid":
        #     speed_estimator = (HybridSpeedEstimator(self.config))

        # else:
        #     raise ValueError(f"Unsupported speed estimator: {algorithm}")

        # Metrics
        metrics = Metrics()
        metrics_exporter = MetricsExporter()

        # Evaluation
        evaluator = Evaluator()

        # Benchmark Configuration
        benchmark_cfg = self.config["benchmark"]
        # benchmark_enabled = benchmark_cfg.get("enabled", False)
        benchmark_type = benchmark_cfg.get("type")
        experiment_name = benchmark_cfg.get("experiment_name")

        # Visualizer
        # if benchmark_enabled:
        visualizer = Visualizer(
            output_video=video_output_path(
                benchmark_cfg["output_directory"], benchmark_type, experiment_name
            ),
            fps=video_loader.fps,
            frame_width=video_loader.width,
            frame_height=video_loader.height,
        )
        # Re-ID

        predictor = VehicleReIDPredictor(
            checkpoint_path=str(checkpoint_path),
        )

        vehicle_database = VehicleDatabase()

        track_adapter = Track1Adapter(
            lost_threshold=30,
        )

        reid_manager = ReIDManager(
            predictor=predictor,
            database=vehicle_database,
        )
        reid_post_processor = ReIDPostProcessor(
            adapter=track_adapter,
            reid_manager=reid_manager,
        )
        reid_exporter = ReIDExporter()
        gallery_exporter = GalleryExporter()
        # Pipeline
        pipeline = Pipeline(
            video_loader=video_loader,
            detector=detector,
            tracker=tracker,
            # trajectory_manager=trajectory_manager,
            # speed_estimator=speed_estimator,
            metrics=metrics,
            evaluator=evaluator,
            visualizer=visualizer,
            post_processors=[
                reid_post_processor,
            ],
        )

        try:
            summary = pipeline.run()
        finally:
            video_loader.release()  # runs even if pipeline fails

        output_path = (
            Path(benchmark_cfg["output_directory"]) / "reid" / "reid_results.json"
        )

        reid_exporter.export(
            results=reid_post_processor.results,
            json_path=output_path,
        )
        gallery_exporter.export(
            records=reid_post_processor.gallery_records,
            output_directory=(
                Path(benchmark_cfg["output_directory"]) / "reid" / "gallery"
            ),
        )
        # Export
        # exporting results in only json format for now, cdsv can also be generated
        metrics_exporter.export(
            summary,
            # csv_path=csv_output_path(
            #     benchmark_cfg["output_directory"],
            #     benchmark_type,
            #     experiment_name,
            # ),
            json_path=json_output_path(
                benchmark_cfg["output_directory"],
                benchmark_type,
                experiment_name,
            ),
        )

        return summary
