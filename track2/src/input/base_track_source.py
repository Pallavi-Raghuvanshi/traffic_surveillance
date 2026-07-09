# ============================================================================
# base_track_source.py
# ============================================================================

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from core.schemas import FrameTracks


class BaseTrackSource(ABC):
    """
    Abstract interface for anything that can feed Component 2 with
    per-frame track data.

    Component 2 is completely decoupled from how these tracks were
    produced — a live detector/tracker, a recorded export file, or any
    future streaming feed — as long as it can be iterated as a
    sequence of `FrameTracks`.
    """

    @abstractmethod
    def __iter__(
        self,
    ) -> Iterator[FrameTracks]:

        raise NotImplementedError

    @property
    @abstractmethod
    def fps(
        self,
    ) -> float:
        """
        Frame rate of the underlying source, used only for reporting
        and for time-window-to-frame-count conversions in benchmarks.
        """

        raise NotImplementedError

    def close(
        self,
    ) -> None:
        """
        Release any underlying resources.

        Most sources have nothing to release, so the default
        implementation performs no action.
        """

        return
