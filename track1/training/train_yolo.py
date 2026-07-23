# train_yolo.py
# ============================================================================
# Trains a YOLO model on the converted UA-DETRAC dataset
# ============================================================================

from __future__ import annotations
from pathlib import Path
from ultralytics import YOLO


class YOLOTrainer:
    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[1]

        self.dataset_yaml = (
            project_root / "datasets" / "UA-DETRAC-YOLO" / "dataset.yaml"
        )
        self.model_name = "yolo11n.pt"
        self.epochs = 100
        self.image_size = 640
        self.batch_size = -1
        self.workers = 4
        self.device = "0"
        self.project = "runs/train"
        self.experiment_name = "yolo11n_detrac"

    def train(self) -> None:
        if not self.dataset_yaml.exists():
            raise FileNotFoundError(f"Dataset yaml not found:\n{self.dataset_yaml}")
        print("=" * 60)
        print("Loading Model")
        print("=" * 60)
        model = YOLO(self.model_name)
        print("=" * 60)
        print("Training Started")
        print("=" * 60)
        results = model.train(
            data=str(self.dataset_yaml),
            epochs=self.epochs,
            imgsz=self.image_size,
            batch=self.batch_size,
            workers=self.workers,
            device=self.device,
            project=self.project,
            name=self.experiment_name,
            exist_ok=True,
            pretrained=True,
            verbose=True,
            cache=False,
        )
        print("=" * 60)
        print("Training Completed")
        print("=" * 60)
        weights_dir = Path(self.project) / self.experiment_name / "weights"
        print(f"Best weights : {results.save_dir}/weights/best.pt")
        print(f"Last weights : {results.save_dir}/weights/last.pt")

    def validate(self) -> None:
        model = YOLO(Path(self.project) / self.experiment_name / "weights" / "best.pt")
        metrics = model.val(
            data=str(self.dataset_yaml),
            split="test",
        )
        print("=" * 60)
        print("Validation Results")
        print("=" * 60)
        print(metrics)
        print(f"mAP50      : {metrics.box.map50:.4f}")
        print(f"mAP50-95   : {metrics.box.map:.4f}")
        print(f"Precision  : {metrics.box.mp:.4f}")
        print(f"Recall     : {metrics.box.mr:.4f}")


if __name__ == "__main__":
    trainer = YOLOTrainer()
    trainer.train()
    trainer.validate()
