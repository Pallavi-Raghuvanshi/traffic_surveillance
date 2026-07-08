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
    Traffic Surveillance entry point.

    Parameters
    ----------
    config
        Optional configuration instance.

    Returns
    -------
    BenchmarkSummary
        Benchmark summary generated after execution.
    """

    logger.info(
        "Traffic Surveillance Started"
    )

    try:

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

    except Exception:

        logger.exception(
            "Traffic Surveillance Failed."
        )

        raise


if __name__ == "__main__":

    main()