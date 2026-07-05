# config.py
from pathlib import Path

import yaml
from pydantic import BaseModel


# -----------------------------
# Individual configuration sections
# -----------------------------

class ProjectConfig(BaseModel):
    name: str
    version: str


class PathsConfig(BaseModel):
    video: str
    output_dir: str
    model_dir: str


class VideoConfig(BaseModel):
    process_fps: int
    display: bool


class LoggingConfig(BaseModel):
    level: str


# -----------------------------
# Main configuration model
# -----------------------------

class AppConfig(BaseModel):
    project: ProjectConfig
    paths: PathsConfig
    video: VideoConfig
    logging: LoggingConfig


# -----------------------------
# Configuration Loader
# -----------------------------

class Config:

    def __init__(self,
                 config_path: str = "configs/config.yaml"):

        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with config_path.open("r", encoding="utf-8") as file:
            config_dict = yaml.safe_load(file)

        self.settings = AppConfig(**config_dict)

    def __getattr__(self, item):
        """
        Allows:
            config.video
            config.paths
            config.project
        """
        return getattr(self.settings, item)