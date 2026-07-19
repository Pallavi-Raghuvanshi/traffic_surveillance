# config.py
# Loads and provides access to the project configuration (config.yaml).
# ============================================================================

from __future__ import annotations # Stores type hints as strings instead of immediately evaluating them
from pathlib import Path # makes handling file paths much easier
from typing import Any 
import yaml # converts YAML text format into standard Python dictionaries and lists

class Config:
    """Supports:

    config["tracking"]
    config.get(...)
    """

    DEFAULT_CONFIG = ( Path(__file__).resolve().parents[1] / "config.yaml")

    def __init__(self) -> None: # Type hints: config_path can be string, path object 
        
        self._config_path = self._resolve_path("config.yaml")
        
        if not self._config_path.exists():
            raise FileNotFoundError(f"Configuration file not found:\n {self._config_path}")
        
        with self._config_path.open("r", encoding="utf-8") as file:
            settings = yaml.safe_load(file)
        
        if not isinstance(settings, dict):
            raise ValueError("Configuration must contain a YAML mapping.")
        
        self._settings: dict[str, Any] = settings
        
    # When object's representation needed, it is automatically called.
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path='{self._config_path}')"
    
    # Whenever Python sees config[..]
    def __getitem__(self, key: str) -> Any:
        return self._settings[key]

    # return default value instead of raising any exception
    def get(self, key: str, default: Any = None) -> Any: # if no value provided for default in function call, 'None' used
        return self._settings.get(key, default)
        
    # Whenever Python sees 'key in config' or 'key not in config'
    def __contains__(self, key: str) -> bool:
        return key in self._settings
    
    @classmethod
    def _resolve_path(cls, config_path: str | Path | None) -> Path:
        if config_path is None:
            return cls.DEFAULT_CONFIG.resolve()

        config_path = Path(config_path)
        if config_path.is_absolute():
            return config_path.resolve()

        return (Path(__file__).resolve().parents[2] / config_path).resolve()