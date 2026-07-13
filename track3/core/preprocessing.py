from __future__ import annotations

import cv2
import numpy as np
import torch
from torchvision import transforms

from track3.core.config import CONFIG


class ImagePreprocessor:
    """
    Preprocesses OpenCV vehicle images for OSNet inference.

    Input
    -----
    OpenCV image (BGR)

    Output
    ------
    Torch tensor of shape (1, 3, H, W)
    """

    def __init__(self) -> None:

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=CONFIG.imagenet_mean,
                std=CONFIG.imagenet_std,
            )
        ])

    def __call__(self, image: np.ndarray) -> torch.Tensor:
        """
        Convert an OpenCV BGR image into a tensor suitable for OSNet.
        """

        if image is None:
            raise ValueError("Input image is None.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.resize(
            image,
            CONFIG.input_size,
            interpolation=cv2.INTER_LINEAR,
        )

        image = self.transform(image)

        image = image.unsqueeze(0)

        return image