from dataclasses import dataclass

from src.embedding.models.settings import Settings

@dataclass
class Embedding:
    model: str
    settings: Settings

    @classmethod
    def from_dict(cls, config: dict):
        if "model" not in config or not config["model"]:
            raise ValueError("Embedding model is required")

        if "settings" not in config or not config["settings"]:
            raise ValueError("Embedding settings are required")

        settings = Settings.from_dict(config["settings"])

        return cls(
            model=config["model"],
            settings=settings
        )