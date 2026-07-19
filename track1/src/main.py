# main.py
# ============================================================================

from __future__ import annotations
import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=r".*ByteTrack.*deprecated.*",
)

from core.config import Config
from core.logger import get_logger

from evaluation.benchmark_summary import BenchmarkSummary
from experiments import ExperimentRunner

logger = get_logger(__name__)

def main(config: Config | None = None) -> BenchmarkSummary:
    logger.info("Traffic Surveillance Started")
    try:
        if config is None:
            config = Config()
        runner = ExperimentRunner(config)
        summary = runner.run()
        logger.info("Traffic Surveillance Finished")
        return summary
    except Exception:
        logger.exception("Traffic Surveillance Failed.")
        raise

if __name__ == "__main__":
    main()