# ============================================================================
# flow_model.py
#
# Learns the dominant traffic-flow direction directly from observed
# track motion, with no manually defined lanes or calibration.
#
# The frame is partitioned into a grid of fixed-size pixel cells. Each
# cell accumulates an exponentially-weighted average of the unit
# direction vectors of vehicles that have moved through it. Once a
# cell has seen enough samples, its blended vector is treated as the
# "dominant" direction of travel for that region of the road.
# ============================================================================

from __future__ import annotations

from utils.geometry import vector_heading, vector_magnitude

from engine.track_history import MotionState


Point = tuple[float, float]
Vector = tuple[float, float]
CellKey = tuple[int, int]


class DominantFlowModel:
    """
    Learns per-region dominant traffic-flow direction from historical
    track motion.

    This model is purely descriptive of *observed* motion — it makes
    no assumption about lane geometry, road direction, or calibration.
    """

    def __init__(
        self,
        *,
        cell_size_px: float,
        ema_alpha: float,
        min_samples: int,
        min_motion_speed: float,
    ) -> None:

        self._cell_size = max(1.0, cell_size_px)

        self._ema_alpha = ema_alpha

        self._min_samples = min_samples

        self._min_motion_speed = min_motion_speed

        self._cell_vectors: dict[CellKey, Vector] = {}

        self._cell_samples: dict[CellKey, int] = {}

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        motion_states: dict[int, MotionState],
    ) -> None:

        for state in motion_states.values():

            if state.speed < self._min_motion_speed:

                continue

            if state.heading is None:

                continue

            unit_vector = (

                state.velocity[0] / state.speed,

                state.velocity[1] / state.speed,
            )

            key = self._cell_key(state.centroid)

            self._blend(key, unit_vector)

            self._cell_samples[key] = (
                self._cell_samples.get(key, 0) + 1
            )

    def _blend(
        self,
        key: CellKey,
        unit_vector: Vector,
    ) -> None:

        existing = self._cell_vectors.get(key)

        if existing is None:

            self._cell_vectors[key] = unit_vector

            return

        alpha = self._ema_alpha

        blended = (

            existing[0] * (1.0 - alpha) + unit_vector[0] * alpha,

            existing[1] * (1.0 - alpha) + unit_vector[1] * alpha,
        )

        self._cell_vectors[key] = blended

    def _cell_key(
        self,
        point: Point,
    ) -> CellKey:

        return (

            int(point[0] // self._cell_size),

            int(point[1] // self._cell_size),
        )

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #

    def dominant_heading(
        self,
        point: Point,
    ) -> float | None:
        """
        Learned dominant travel direction (radians) for the region
        containing `point`, or None if that region has not yet
        accumulated enough samples to be considered reliable.
        """

        key = self._cell_key(point)

        if self._cell_samples.get(key, 0) < self._min_samples:

            return None

        vector = self._cell_vectors.get(key)

        if vector is None or vector_magnitude(vector) < 1e-9:

            return None

        return vector_heading(vector)

    def has_dominant_flow(
        self,
        point: Point,
    ) -> bool:

        return self.dominant_heading(point) is not None

    def clear(
        self,
    ) -> None:

        self._cell_vectors.clear()

        self._cell_samples.clear()
