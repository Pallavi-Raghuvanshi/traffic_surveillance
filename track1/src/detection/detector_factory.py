# detector_factory.py

from base_detector.yolo_detector import YOLODetector


class DetectorFactory:
    """
    Creates detector instances.

    Later this class will support:

    YOLO11

    YOLO26

    FasterRCNN

    RT-DETR

    DINO
    """

    @staticmethod
    def create(config):

        model_name = (
            config["detection"]["model"]
            .lower()
        )

        if model_name.startswith("yolo"):
            return YOLODetector(config)

        raise ValueError(
            f"Unsupported detector: {model_name}"
        )