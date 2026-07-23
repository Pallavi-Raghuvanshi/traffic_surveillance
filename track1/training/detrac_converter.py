# ============================================================================
# detrac_converter.py
# ============================================================================
"""
UA-DETRAC Dataset Converter

Responsibilities
----------------
1. Identify annotated and unannotated sequences.
2. Move/copy unannotated sequences to inference/.
3. Split annotated sequences into train/validation.
4. Convert annotations into YOLO format.
5. Generate dataset.yaml.
"""

from __future__ import annotations
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


class DetracConverter:
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    CLASS_MAPPING = {
        "bicycle": 0,
        "car": 1,
        "motorcycle": 2,
        "bus": 3,
        "truck": 4,
    }

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[1]

        self.dataset_root = project_root / "datasets"

        # Actual folders
        self.images_dir = (
            self.dataset_root
            / "DETRAC-Images"
            / "DETRAC-Images"
        )

        self.annotations_dir = (
            self.dataset_root
            / "DETRAC-Train-Annotations-XML"
            / "DETRAC-Train-Annotations-XML"
        )

        self.test_annotations_dir = (
            self.dataset_root
            / "DETRAC-Test-Annotations-XML"
            / "DETRAC-Test-Annotations-XML"
        )

        # Folder to store test sequences without annotations
        # self.inference_dir = self.dataset_root / "DETRAC-Inference"

        # YOLO dataset
        self.output_root = self.dataset_root / "UA-DETRAC-YOLO"

        self.train_ratio = 0.9
        self.random_seed = 42
        self.frame_stride = 5
        self.train_sequences: list[str] = []
        self.val_sequences: list[str] = []
        self.test_sequences: list[str] = []

    def convert(self) -> None:

        annotated, inference = self._discover_sequences()

        self.train_sequences, self.val_sequences = self._split_sequences(annotated)

        self.test_sequences = sorted(
            xml.stem for xml in self.test_annotations_dir.glob("*.xml")
        )

        self._prepare_output_folders()

        self._convert_split(
            self.train_sequences,
            split="train",
            annotation_dir=self.annotations_dir,
        )

        self._convert_split(
            self.val_sequences,
            split="val",
            annotation_dir=self.annotations_dir,
        )

        self._convert_split(
            self.test_sequences,
            split="test",
            annotation_dir=self.test_annotations_dir,
        )

        self._generate_dataset_yaml()

    def _discover_sequences(self) -> tuple[list[str], list[str]]:
        """
        Returns
        -------
        annotated_sequences
        inference_sequences
        """

        image_sequences = {
            folder.name for folder in self.images_dir.iterdir() if folder.is_dir()
        }

        train_annotations = {xml.stem for xml in self.annotations_dir.glob("*.xml")}

        test_annotations = {xml.stem for xml in self.test_annotations_dir.glob("*.xml")}

        train_sequences = sorted(image_sequences & train_annotations)
        test_sequences = sorted(image_sequences & test_annotations)

        print(f"Training sequences : {len(train_sequences)}")
        print(f"Test sequences     : {len(test_sequences)}")

        return train_sequences, test_sequences

    # def _prepare_inference_dataset(self, sequences: list[str]) -> None:
    #     """Copies every unannotated sequence into UA-DETRAC/inference/"""
    #     for sequence in sequences:
    #         source = self.images_dir / sequence
    #         destination = self.inference_dir / sequence
    #         if destination.exists():
    #             shutil.rmtree(destination)
    #         shutil.copytree(source, destination)

    def _split_sequences(self, sequences: list[str]) -> tuple[list[str], list[str]]:
        rng = random.Random(self.random_seed)
        shuffled = list(sequences)
        rng.shuffle(shuffled)
        split_index = int(len(shuffled) * self.train_ratio)
        train = shuffled[:split_index]
        val = shuffled[split_index:]
        print()
        print(f"Train sequences : {len(train)}")
        print(f"Validation sequences : {len(val)}")
        return train, val

    def _prepare_output_folders(self) -> None:

        folders = [
            self.output_root / "images" / "train",
            self.output_root / "images" / "val",
            self.output_root / "images" / "test",
            self.output_root / "labels" / "train",
            self.output_root / "labels" / "val",
            self.output_root / "labels" / "test",
        ]

        for folder in folders:
            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

    @staticmethod
    def _image_files(sequence_dir: Path) -> list[Path]:
        return sorted(
            image
            for image in sequence_dir.iterdir()
            if image.suffix.lower() in DetracConverter.IMAGE_EXTENSIONS
        )

    @staticmethod
    def _frame_number(image_path: Path) -> int:
        return int(image_path.stem.replace("img", ""))

    @staticmethod
    def _prefixed_filename(sequence: str, filename: str) -> str:
        return f"{sequence}_{filename}"

    def _convert_split(
        self,
        sequences: list[str],
        split: str,
        annotation_dir: Path,
    ) -> None:
        image_output_dir = self.output_root / "images" / split
        label_output_dir = self.output_root / "labels" / split
        for sequence in sequences:
            print(f"Processing {sequence} ({split})")
            xml_file = annotation_dir / f"{sequence}.xml"
            image_dir = self.images_dir / sequence
            frame_annotations = self._parse_xml(xml_file)
            image_lookup = {
                frame: objects for frame, objects in frame_annotations.items()
            }

            for image_path in self._image_files(image_dir):
                frame_number = self._frame_number(image_path)
                if frame_number % self.frame_stride != 1:
                    continue
                destination_name = self._prefixed_filename(sequence, image_path.name)
                destination_image = image_output_dir / destination_name
                shutil.copy2(image_path, destination_image)
                label_file = label_output_dir / destination_name.replace(".jpg", ".txt")
                annotations = image_lookup.get(frame_number, [])
                self._write_label_file(label_file, annotations)

    def _parse_xml(self, xml_file: Path) -> dict[int, list[dict]]:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        annotations = {}
        for frame in root.findall("frame"):
            frame_number = int(frame.attrib["num"])
            if frame_number % self.frame_stride != 1:
                continue
            objects = []
            target_list = frame.find("target_list")
            if target_list is not None:
                for target in target_list.findall("target"):
                    box = target.find("box")
                    attribute = target.find("attribute")
                    if box is None or attribute is None:
                        continue
                    vehicle_type = attribute.attrib["vehicle_type"]
                    if vehicle_type not in self.CLASS_MAPPING:
                        continue
                    objects.append(
                        {
                            # Target ID
                            "target_id": int(target.attrib["id"]),
                            # Bounding Box
                            "left": float(box.attrib["left"]),
                            "top": float(box.attrib["top"]),
                            "width": float(box.attrib["width"]),
                            "height": float(box.attrib["height"]),
                            # Attributes
                            "class": attribute.attrib["vehicle_type"],
                            "orientation": float(attribute.attrib["orientation"]),
                            "speed": float(attribute.attrib["speed"]),
                            "trajectory_length": int(
                                attribute.attrib["trajectory_length"]
                            ),
                            "truncation_ratio": float(
                                attribute.attrib["truncation_ratio"]
                            ),
                            # Occlusion (filled below)
                            "occlusion": False,
                            "occlusion_id": None,
                            "occlusion_status": None,
                            "occlusion_left": None,
                            "occlusion_top": None,
                            "occlusion_width": None,
                            "occlusion_height": None,
                        }
                    )
            annotations[frame_number] = objects
        return annotations

    @staticmethod
    def _image_size(image_path: Path) -> tuple[int, int]:
        import cv2

        image = cv2.imread(str(image_path))
        height, width = image.shape[:2]
        return width, height

    def _write_label_file(self, label_path: Path, annotations: list[dict]) -> None:
        image_name = label_path.stem.split("_", 2)[-1] + ".jpg"
        sequence = label_path.stem.rsplit("_", 1)[0]
        image_path = self.images_dir / sequence / image_name
        image_width, image_height = self._image_size(image_path)
        with open(label_path, "w") as file:
            for obj in annotations:
                x_center = (obj["left"] + obj["width"] / 2) / image_width
                y_center = (obj["top"] + obj["height"] / 2) / image_height
                width = obj["width"] / image_width
                height = obj["height"] / image_height
                class_id = self.CLASS_MAPPING[obj["class"]]
                file.write(
                    f"{class_id} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}\n"
                )

    def _generate_dataset_yaml(self) -> None:

        yaml_path = self.output_root / "dataset.yaml"

        names = sorted(
            self.CLASS_MAPPING,
            key=self.CLASS_MAPPING.get,
        )

        with open(yaml_path, "w") as file:

            file.write(f"path: {self.output_root.resolve()}\n")

            file.write("train: images/train\n")
            file.write("val: images/val\n")
            file.write("test: images/test\n\n")

            file.write(f"nc: {len(names)}\n")
            file.write(f"names: {names}\n")

        print()
        print("dataset.yaml generated.")
        print("Conversion complete.")


if __name__ == "__main__":
    converter = DetracConverter()
    converter.convert()
    print("\nDataset conversion completed successfully.")
