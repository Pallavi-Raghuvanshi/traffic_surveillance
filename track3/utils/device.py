import torch


def get_device(preferred: str = "cuda") -> torch.device:
    """
    Returns the best available execution device.

    Parameters
    ----------
    preferred:
        Preferred execution device ("cuda" or "cpu").

    Returns
    -------
    torch.device
        CUDA device if available and requested,
        otherwise CPU.
    """

    preferred = preferred.lower()

    if preferred == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")