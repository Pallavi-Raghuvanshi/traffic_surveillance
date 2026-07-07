# ============================================================================
# main.py
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.logger import get_logger

from evaluation.benchmark_summary import BenchmarkSummary

from experiments import (
    ExperimentRunner,
)


logger = get_logger(__name__)


def main(
    config: Config | None = None,
) -> BenchmarkSummary:
    """
    Project entry point.

    Returns
    -------
    BenchmarkSummary
        Summary generated after pipeline execution.
    """

    logger.info(
        "Traffic Surveillance Started"
    )

    if config is None:

        config = Config()

    runner = ExperimentRunner(
        config
    )

    summary = runner.run()

    logger.info(
        "Traffic Surveillance Finished"
    )

    return summary


if __name__ == "__main__":

    main()