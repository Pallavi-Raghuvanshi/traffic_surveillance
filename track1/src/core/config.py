# ============================================================================
# config.py
#
# Description:
#     Configuration loader for the Traffic Surveillance System.
# ============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class Config:
    """
    Loads configuration from YAML and provides both
    dictionary-style and attribute-style access.

    Examples
    --------
    config["tracking"]["frame_rate"]

    config["detection"]["weights"]

    config.project["name"]
    """

    def __init__(
        self,
        config_path: str | Path = "configs/config.yaml",
    ) -> None:

        self._config_path = Path(config_path)

        if not self._config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self._config_path}"
            )

        with self._config_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            self._settings: dict[str, Any] = yaml.safe_load(file)

    # ------------------------------------------------------------------
    # Dictionary Access
    # ------------------------------------------------------------------

    def __getitem__(
        self,
        key: str,
    ) -> Any:

        return self._settings[key]

    # ------------------------------------------------------------------
    # Attribute Access
    # ------------------------------------------------------------------

    def __getattr__(
        self,
        item: str,
    ) -> Any:

        try:
            return self._settings[item]

        except KeyError as exc:

            raise AttributeError(
                f"No configuration section named '{item}'."
            ) from exc

    # ------------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._settings.get(
            key,
            default,
        )

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

    def __contains__(
        self,
        key: str,
    ) -> bool:

        return key in self._settings

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(path='{self._config_path}')"
        )