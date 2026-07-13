from __future__ import annotations

import torch.nn as nn


class ReIDLoss(nn.Module):
    """
    Cross Entropy loss for Vehicle Re-ID training.
    """

    def __init__(self):

        super().__init__()

        self.loss = nn.CrossEntropyLoss()

    def forward(
        self,
        logits,
        labels,
    ):

        return self.loss(
            logits,
            labels,
        )