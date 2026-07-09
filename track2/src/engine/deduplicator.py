# ============================================================================
# deduplicator.py
#
# Suppresses repeated emission of the same ongoing anomaly.
#
# Detectors are deliberately kept simple and may re-evaluate the same
# condition on consecutive frames. The deduplicator is the single place
# that decides whether a newly raised event is a genuinely new
# occurrence or a continuation of one already reported, based on a
# cooldown window keyed by (anomaly type, involved track ids).
# ============================================================================

from __future__ import annotations

from core.schemas import AnomalyEvent


DedupKey = tuple[str, frozenset[int]]


class AnomalyDeduplicator:
    """
    Cooldown-based suppression of duplicate anomaly events.
    """

    def __init__(
        self,
        *,
        cooldown_seconds: float,
    ) -> None:

        self._cooldown_seconds = cooldown_seconds

        self._last_emitted: dict[DedupKey, float] = {}

    # ------------------------------------------------------------------ #
    # Filtering
    # ------------------------------------------------------------------ #

    def filter(
        self,
        events: list[AnomalyEvent],
    ) -> list[AnomalyEvent]:
        """
        Return only the events that are not within the cooldown window
        of a previously emitted event of the same type and track set.
        """

        accepted: list[AnomalyEvent] = []

        for event in events:

            key = self._key(event)

            last_timestamp = self._last_emitted.get(key)

            if (

                last_timestamp is not None

                and (event.timestamp - last_timestamp) < self._cooldown_seconds

            ):

                continue

            self._last_emitted[key] = event.timestamp

            accepted.append(event)

        return accepted

    @staticmethod
    def _key(
        event: AnomalyEvent,
    ) -> DedupKey:

        return (

            event.anomaly_type.value,

            frozenset(event.track_ids),
        )

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def clear(
        self,
    ) -> None:

        self._last_emitted.clear()
