# ============================================================================
# tracking/botsort/__init__.py
# ============================================================================

"""
Official Ultralytics BoT-SORT integration.

This package isolates every Ultralytics-specific dependency
from the rest of the traffic surveillance framework.
"""

from .config import (
    build_botsort_args,
)

__all__ = [
    "build_botsort_args",
]