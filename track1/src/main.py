# ============================================================================
# main.py
# ============================================================================

from __future__ import annotations

from core.config import Config

from core.logger import get_logger

from experiments import ExperimentRunner


logger = get_logger(__name__)


def main() -> None:

    logger.info(
        "Traffic Surveillance Started"
    )

    config = Config()

    runner = ExperimentRunner(
        config
    )

    runner.run()

    logger.info(
        "Traffic Surveillance Finished"
    )


if __name__ == "__main__":

    main()