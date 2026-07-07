# ============================================================================
# file_utils.py
# ============================================================================

from __future__ import annotations

from pathlib import Path


def ensure_directory(
    path: str | Path,
) -> Path:
    """
    Create a directory if it does not exist.

    Parameters
    ----------
    path : str | Path
        Directory path.

    Returns
    -------
    Path
        Path object to the created/existing directory.
    """

    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def experiment_directory(
    output_root: str | Path,
    experiment_name: str,
) -> Path:
    """
    Create an experiment output directory.

    Example
    -------
    outputs/
        detector_benchmark/
            yolo11/
    """

    return ensure_directory(
        Path(output_root)
        / "detector_benchmark"
        / experiment_name
    )


def video_output_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:
    """
    Output annotated video path.
    """

    return (
        experiment_directory(
            output_root,
            experiment_name,
        )
        / "annotated.mp4"
    )


def csv_output_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:
    """
    Output detection csv path.
    """

    return (
        experiment_directory(
            output_root,
            experiment_name,
        )
        / "detections.csv"
    )


def json_output_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:
    """
    Output metrics json path.
    """

    return (
        experiment_directory(
            output_root,
            experiment_name,
        )
        / "metrics.json"
    )


def benchmark_csv_path(
    output_root: str | Path,
) -> Path:
    """
    Overall benchmark results.
    """

    return (
        ensure_directory(
            Path(output_root)
            / "detector_benchmark"
        )
        / "detector_results.csv"
    )