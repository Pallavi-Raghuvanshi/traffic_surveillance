# ============================================================================
# config.py
#
# Loads and provides access to the project configuration.
# ============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class Config:
    """
    Loads configuration from YAML.

    Supports:

        config["tracking"]

        config.tracking

        config.get(...)
    """

    DEFAULT_CONFIG = (

        Path(__file__).resolve().parents[2]

        / "configs"

        / "config.yaml"
    )

    def __init__(
        self,
        config_path: str | Path | None = None,
    ) -> None:

        self._config_path = self._resolve_path(
            config_path
        )

        if not self._config_path.exists():

            raise FileNotFoundError(

                "Configuration file not found:\n"
                f"{self._config_path}"
            )

        with self._config_path.open(

            "r",

            encoding="utf-8",
        ) as file:

            settings = yaml.safe_load(
                file
            )

        if not isinstance(
            settings,
            dict,
        ):

            raise ValueError(
                "Configuration must contain "
                "a YAML mapping."
            )

        self._settings: dict[
            str,
            Any,
        ] = settings

    # ------------------------------------------------------------------ #
    # Path Resolution
    # ------------------------------------------------------------------ #

    @classmethod
    def _resolve_path(
        cls,
        config_path: str | Path | None,
    ) -> Path:

        if config_path is None:

            return cls.DEFAULT_CONFIG.resolve()

        config_path = Path(
            config_path
        )

        if config_path.is_absolute():

            return config_path.resolve()

        return (

            Path(__file__)
            .resolve()
            .parents[2]

            / config_path

        ).resolve()

    # ------------------------------------------------------------------ #
    # Dictionary Interface
    # ------------------------------------------------------------------ #

    def __getitem__(
        self,
        key: str,
    ) -> Any:

        return self._settings[key]

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._settings.get(
            key,
            default,
        )

    def __contains__(
        self,
        key: str,
    ) -> bool:

        return key in self._settings

    # ------------------------------------------------------------------ #
    # Attribute Interface
    # ------------------------------------------------------------------ #

    def __getattr__(
        self,
        name: str,
    ) -> Any:

        try:

            return self._settings[
                name
            ]

        except KeyError as exc:

            raise AttributeError(

                f"No configuration section named "
                f"'{name}'."

            ) from exc

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def settings(
        self,
    ) -> dict[str, Any]:

        return self._settings

    @property
    def path(
        self,
    ) -> Path:

        return self._config_path

    # ------------------------------------------------------------------ #
    # Representation
    # ------------------------------------------------------------------ #

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(path='{self._config_path}')"
        )