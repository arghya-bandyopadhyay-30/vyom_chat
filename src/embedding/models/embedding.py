from dataclasses import dataclass

@dataclass
class Embedding:
    model: str
    model_name: str
    api_key: str

    @classmethod
    def from_dict(cls, config: dict):
        if "model" not in config or not config["model"]:
            raise ValueError("Embedding model is required")

        if "model-name" not in config or not config["model-name"]:
            raise ValueError("Embedding model_name are required")

        if "api-key" not in config or not config["api-key"]:
            raise ValueError("Embedding api_key are required")

        return cls(
            model=config["model"],
            model_name=config["model-name"],
            api_key=config["api-key"]
        )