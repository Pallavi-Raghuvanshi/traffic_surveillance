# ============================================================================
# file_utils.py
# ============================================================================

from __future__ import annotations

from pathlib import Path


# -----------------------------------------------------------------------------
# Directories
# -----------------------------------------------------------------------------

def ensure_directory(
    path: str | Path,
) -> Path:
    """
    Create a directory if it does not already exist.
    """

    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def benchmark_directory(
    output_root: str | Path,
    benchmark_type: str,
) -> Path:
    """
    Example
    -------
    outputs/
        detector_benchmark/

    outputs/
        tracker_benchmark/
    """

    return ensure_directory(
        Path(output_root)
        / f"{benchmark_type}_benchmark"
    )


def experiment_directory(
    output_root: str | Path,
    benchmark_type: str,
    experiment_name: str,
) -> Path:
    """
    Example
    -------
    outputs/
        detector_benchmark/
            yolo11n/

    outputs/
        tracker_benchmark/
            bytetrack/
    """

    return ensure_directory(
        benchmark_directory(
            output_root,
            benchmark_type,
        )
        / experiment_name
    )


# -----------------------------------------------------------------------------
# Experiment Files
# -----------------------------------------------------------------------------

def video_output_path(
    output_root: str | Path,
    benchmark_type: str,
    experiment_name: str,
) -> Path:

    return (
        experiment_directory(
            output_root,
            benchmark_type,
            experiment_name,
        )
        / "annotated.mp4"
    )


def csv_output_path(
    output_root: str | Path,
    benchmark_type: str,
    experiment_name: str,
) -> Path:

    return (
        experiment_directory(
            output_root,
            benchmark_type,
            experiment_name,
        )
        / "metrics.csv"
    )


def json_output_path(
    output_root: str | Path,
    benchmark_type: str,
    experiment_name: str,
) -> Path:

    return (
        experiment_directory(
            output_root,
            benchmark_type,
            experiment_name,
        )
        / "metrics.json"
    )


# -----------------------------------------------------------------------------
# Overall Benchmark Result
# -----------------------------------------------------------------------------

def benchmark_csv_path(
    output_root: str | Path,
    benchmark_type: str,
) -> Path:

    filename = (
        "detector_results.csv"
        if benchmark_type == "detector"
        else "tracker_results.csv"
    )

    return (
        benchmark_directory(
            output_root,
            benchmark_type,
        )
        / filename
    )