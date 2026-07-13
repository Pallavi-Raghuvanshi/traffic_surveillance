from __future__ import annotations

from pathlib import Path

import torch

from track3.models.osnet import OSNetModel


def save_checkpoint(
    model: OSNetModel,
    path: str | Path,
):

    torch.save(
        model.state_dict(),
        path,
    )


def load_checkpoint(
    model: OSNetModel,
    path: str | Path,
):

    state_dict = torch.load(
        path,
        map_location=model.device,
    )

    model.load_state_dict(
        state_dict,
    )

    return model