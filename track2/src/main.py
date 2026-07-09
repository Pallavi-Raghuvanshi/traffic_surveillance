# ============================================================================
# main.py
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.logger import get_logger

from evaluation.benchmark_summary import AnomalyBenchmarkSummary

from experiments import (
    ExperimentRunner,
)


logger = get_logger(__name__)


def main(
    config: Config | None = None,
) -> AnomalyBenchmarkSummary:
    """
    Traffic Anomaly Detection entry point.

    Parameters
    ----------
    config
        Optional configuration instance.

    Returns
    -------
    AnomalyBenchmarkSummary
        Benchmark summary generated after execution.
    """

    logger.info(
        "Traffic Anomaly Detection Started"
    )

    try:

        if config is None:

            config = Config()

        runner = ExperimentRunner(
            config
        )

        summary = runner.run()

        logger.info(
            "Traffic Anomaly Detection Finished"
        )

        return summary

    except Exception:

        logger.exception(
            "Traffic Anomaly Detection Failed."
        )

        raise


if __name__ == "__main__":

    main()
