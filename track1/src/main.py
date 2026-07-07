# ============================================================================
# main.py
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.logger import get_logger

from experiments import ExperimentRunner


logger = get_logger(__name__)


def main(
    config: Config | None = None,
) -> dict | None:
    """
    Project entry point.

    Returns
    -------
    dict | None
        Benchmark summary when benchmarking is enabled,
        otherwise None.
    """

    logger.info(
        "Traffic Surveillance Started"
    )

    if config is None:

        config = Config()

    runner = ExperimentRunner(
        config
    )

    result = runner.run()

    logger.info(
        "Traffic Surveillance Finished"
    )

    return result


if __name__ == "__main__":

    main()