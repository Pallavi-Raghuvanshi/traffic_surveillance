# train_rtdetr.py
# ============================================================================
# Trains an RT-DETR model on the converted UA-DETRAC dataset
# ============================================================================

from __future__ import annotations
from pathlib import Path
from ultralytics import RTDETR

class RTDETRTrainer:
    def __init__(self) -> None:
        self.dataset_yaml = Path("datasets/UA-DETRAC-YOLO/dataset.yaml")
        self.model_name = "rtdetr-l.pt"
        self.epochs = 100
        self.image_size = 640
        self.batch_size = 16
        self.workers = 4
        self.device = 0 # gpu
        self.project = "runs/train"
        self.experiment_name = "rtdetr_detrac"

    def train(self) -> None:
        if not self.dataset_yaml.exists():
            raise FileNotFoundError(f"Dataset yaml not found:\n{self.dataset_yaml}")
        print("=" * 60)
        print("Loading RT-DETR Model")
        print("=" * 60)
        model = RTDETR(self.model_name)
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
        )
        print("=" * 60)
        print("Training Completed")
        print("=" * 60)
        print(f"Best weights : {results.save_dir}/weights/best.pt")
        print(f"Last weights : {results.save_dir}/weights/last.pt")

    def validate(self) -> None:
        model = RTDETR(Path(self.project) / self.experiment_name / "weights" / f"ft_{Path(self.model_name).stem}_detrac.pt")
        metrics = model.val()
        print("=" * 60)
        print("Validation Results")
        print("=" * 60)
        print(metrics)

if __name__ == "__main__":
    trainer = RTDETRTrainer()
    trainer.train()
    trainer.validate()