# ============================================================================
# tracker_factory.py
#
# Description:
#     Factory class responsible for creating tracker instances.
# ============================================================================

from __future__ import annotations

from core.config import Config

from tracking.base_tracker import BaseTracker
from tracking.bytetrack_tracker import ByteTrackTracker


class TrackerFactory:
    """
    Factory responsible for creating tracker objects.

    Supported Trackers
    ------------------
    - ByteTrack

    Future
    ------
    - DeepSORT
    - BoT-SORT
    - OC-SORT
    """

    @staticmethod
    def create(
        config: Config,
    ) -> BaseTracker:
        """
        Create tracker from configuration.
        """

        algorithm = (
            config["tracking"]["algorithm"]
            .strip()
            .lower()
        )

        if algorithm == "bytetrack":
            return ByteTrackTracker(config)

        raise ValueError(
            f"Unsupported tracker: '{algorithm}'"
        )