# ============================================================================
# file_utils.py
# ============================================================================

from __future__ import annotations

from pathlib import Path


# ------------------------------------------------------------------ #
# Directory Utilities
# ------------------------------------------------------------------ #

def ensure_directory(
    path: str | Path,
) -> Path:
    """
    Create a directory if it does not already exist.
    """

    directory = Path(
        path
    )

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
    Return the output directory for a single anomaly-detection run.

    Example
    -------
    outputs/
        anomaly_runs/
            sample/
    """

    return ensure_directory(

        Path(output_root)

        / "anomaly_runs"

        / experiment_name
    )


# ------------------------------------------------------------------ #
# Run Output Files
# ------------------------------------------------------------------ #

def video_output_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:

    return (

        experiment_directory(
            output_root,
            experiment_name,
        )

        / "annotated.mp4"
    )


def events_csv_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:

    return (

        experiment_directory(
            output_root,
            experiment_name,
        )

        / "anomalies.csv"
    )


def events_json_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:

    return (

        experiment_directory(
            output_root,
            experiment_name,
        )

        / "anomalies.json"
    )


def metrics_csv_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:

    return (

        experiment_directory(
            output_root,
            experiment_name,
        )

        / "metrics.csv"
    )


def metrics_json_path(
    output_root: str | Path,
    experiment_name: str,
) -> Path:

    return (

        experiment_directory(
            output_root,
            experiment_name,
        )

        / "metrics.json"
    )


# ------------------------------------------------------------------ #
# Benchmark Summary Files
# ------------------------------------------------------------------ #

def benchmark_directory(
    output_root: str | Path,
) -> Path:

    return ensure_directory(

        Path(output_root)

        / "anomaly_benchmark"
    )


def benchmark_csv_path(
    output_root: str | Path,
) -> Path:

    return (

        benchmark_directory(
            output_root
        )

        / "benchmark_results.csv"
    )


def benchmark_json_path(
    output_root: str | Path,
) -> Path:

    return (

        benchmark_directory(
            output_root
        )

        / "benchmark_results.json"
    )
