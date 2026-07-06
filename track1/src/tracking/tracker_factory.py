# ============================================================================
# tracker_factory.py
# ============================================================================

from __future__ import annotations

from core.config import Config

from tracking.base_tracker import BaseTracker

from tracking.bytetrack_tracker import ByteTrackTracker
from tracking.deepsort_tracker import DeepSORTTracker
from tracking.botsort_tracker import BoTSORTTracker


class TrackerFactory:
    """
    Factory responsible for creating trackers.
    """

    @staticmethod
    def create(
        config: Config,
    ) -> BaseTracker:

        algorithm = (
            config["tracking"]["algorithm"]
            .strip()
            .lower()
        )

        if algorithm == "bytetrack":
            return ByteTrackTracker(config)

        if algorithm == "deepsort":
            return DeepSORTTracker(config)

        if algorithm == "botsort":
            return BoTSORTTracker(config)

        raise ValueError(
            f"Unsupported tracker: {algorithm}"
        )