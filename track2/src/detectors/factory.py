# ============================================================================
# factory.py
#
# Registry-based factory for anomaly detectors.
#
# New anomaly detectors are added by creating a new module under
# `detectors/` and decorating the class with `@AnomalyDetectorFactory.
# register("name")`. Nothing outside that module — and in particular
# nothing in `AnomalyEngine` — needs to change.
# ============================================================================

from __future__ import annotations

from typing import Callable

from core.config import Config
from core.exceptions import DetectorRegistrationError

from detectors.base_anomaly_detector import BaseAnomalyDetector


class AnomalyDetectorFactory:
    """
    Registration and instantiation point for anomaly detectors.
    """

    _registry: dict[str, type[BaseAnomalyDetector]] = {}

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #

    @classmethod
    def register(
        cls,
        name: str,
    ) -> Callable[
        [type[BaseAnomalyDetector]],
        type[BaseAnomalyDetector],
    ]:

        def decorator(
            detector_cls: type[BaseAnomalyDetector],
        ) -> type[BaseAnomalyDetector]:

            cls._registry[name] = detector_cls

            return detector_cls

        return decorator

    # ------------------------------------------------------------------ #
    # Instantiation
    # ------------------------------------------------------------------ #

    @classmethod
    def create(
        cls,
        name: str,
        config: Config,
    ) -> BaseAnomalyDetector:

        try:

            detector_cls = cls._registry[name]

        except KeyError as exc:

            raise DetectorRegistrationError(

                f"No anomaly detector registered under name "
                f"'{name}'. Available: {sorted(cls._registry)}"

            ) from exc

        return detector_cls(config)

    @classmethod
    def create_all(
        cls,
        names: list[str],
        config: Config,
    ) -> list[BaseAnomalyDetector]:

        return [
            cls.create(name, config)
            for name in names
        ]

    # ------------------------------------------------------------------ #
    # Introspection
    # ------------------------------------------------------------------ #

    @classmethod
    def available(
        cls,
    ) -> list[str]:

        return sorted(cls._registry)
