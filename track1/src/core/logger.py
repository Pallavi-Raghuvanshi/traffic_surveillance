# logger.py
# ============================================================================

from __future__ import annotations
import logging

_CONFIGURED = False
def get_logger(name: str) -> logging.Logger:
    """
    Logging configuration is performed only once for the entire application.
    Then, stored in Python's logging system
    subsequently, all logger instances use that configuration.
    """

    global _CONFIGURED
    if not _CONFIGURED: # 1st time False
        logging.basicConfig(
            level=logging.INFO, # INFO, ERROR, DEBUG, CRITICAL
            format=(
                "%(asctime)s | " # 2026-07-14 15:30:21
                "%(levelname)s-8s | " # variable values substituted only when logger called
                "%(name)s-20s | "
                "%(message)s" # logger.info("Pipeline started") -> Pipeline started
            ),
        )
        _CONFIGURED = True
    return logging.getLogger(name)