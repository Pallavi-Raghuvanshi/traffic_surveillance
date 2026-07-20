# main.py
# ============================================================================

from __future__ import annotations
import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=r".*ByteTrack.*deprecated.*",
)
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from src.core.config import Config
from src.core.logger import get_logger

from src.evaluation.benchmark_summary import BenchmarkSummary
from src.experiments import ExperimentRunner

logger = get_logger(__name__)

def main() -> BenchmarkSummary:
    logger.info("Traffic Surveillance Started")
    try:
        
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