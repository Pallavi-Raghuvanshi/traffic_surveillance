from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ReIDConfig:
    """Configuration for Vehicle Re-Identification inference."""

    model_name: str = "osnet_x1_0"

    weights_path: Path = Path(
        "track3/weights/osnet_x1_0_msmt17.pth"
    )

    preferred_device: str = "cuda"

    input_size: tuple[int, int] = (256, 256)

    imagenet_mean: tuple[float, float, float] = (
        0.485,
        0.456,
        0.406,
    )

    imagenet_std: tuple[float, float, float] = (
        0.229,
        0.224,
        0.225,
    )


CONFIG = ReIDConfig()