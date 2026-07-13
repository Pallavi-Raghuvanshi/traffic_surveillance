from __future__ import annotations

from pathlib import Path

from PIL import Image
from torch.utils.data import Dataset


class VeRiDataset(Dataset):
    """
    VeRi-776 Dataset.

    Parameters
    ----------
    root
        Root directory of VeRi-776.

    split
        "train", "query", or "gallery".

    transform
        Image transform.

    training
        If True, returns contiguous labels for CrossEntropy.
        If False, returns original vehicle IDs for evaluation.
    """

    def __init__(
        self,
        root: str | Path,
        split: str,
        transform=None,
        training: bool = False,
    ) -> None:

        self.root = Path(root)
        self.transform = transform
        self.training = training

        split_map = {
            "train": "image_train",
            "query": "image_query",
            "gallery": "image_test",
        }

        if split not in split_map:
            raise ValueError(f"Unknown split: {split}")

        self.image_dir = self.root / split_map[split]

        self.images = sorted(self.image_dir.glob("*.jpg"))

        if not self.images:
            raise RuntimeError(f"No images found in {self.image_dir}")

        # Build label mapping only for training
        self.vehicle_ids = sorted({
            int(image.stem.split("_")[0])
            for image in self.images
        })

        self.id_to_label = {
            vehicle_id: index
            for index, vehicle_id in enumerate(self.vehicle_ids)
        }

        self.num_classes = len(self.vehicle_ids)

    def __len__(self):

        return len(self.images)

    def __getitem__(self, index):

        image_path = self.images[index]

        image = Image.open(image_path).convert("RGB")

        vehicle_id = int(image_path.stem.split("_")[0])

        camera_id = int(image_path.stem.split("_")[1][1:])

        if self.training:
            label = self.id_to_label[vehicle_id]
        else:
            label = vehicle_id

        if self.transform is not None:
            image = self.transform(image)

        return {
            "image": image,
            "vehicle_id": label,
            "camera_id": camera_id,
            "path": str(image_path),
        }