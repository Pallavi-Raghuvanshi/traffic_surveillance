from __future__ import annotations

import torch
from torch import Tensor
from torch import nn

from torchreid.models import build_model

from track3.core.config import CONFIG
from track3.utils.device import get_device


class OSNetModel(nn.Module):

    def __init__(
        self,
        num_classes: int,
        loss: str = "softmax",
    ) -> None:

        super().__init__()

        self.device = get_device(CONFIG.preferred_device)

        self.model = build_model(
            name=CONFIG.model_name,
            num_classes=num_classes,
            loss=loss,
            pretrained=True,
            use_gpu=self.device.type == "cuda",
        )

        self.model.to(self.device)

    @property
    def embedding_dimension(self) -> int:
        return 512

    def forward(
        self,
        images: Tensor,
    ) -> Tensor:

        images = images.to(self.device)

        return self.model(images)
