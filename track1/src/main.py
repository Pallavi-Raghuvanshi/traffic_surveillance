from src.core.config import Config

config = Config()

print(config.project.name)
print(config.project.version)

print(config.paths.video)

print(config.video.process_fps)

print(config.logging.level)