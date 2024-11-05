from dataclasses import dataclass

@dataclass
class Embedding:
    model: str
    model_name: str
    api_key: str

    @classmethod
    def from_dict(cls, config: dict):
        required_fields = ["model", "model-name", "api-key"]
        for field in required_fields:
            if field not in config or not config[field]:
                raise ValueError(f"Embedding configuration: '{field}' is required")

        return cls(
            model=config["model"],
            model_name=config["model-name"],
            api_key=config["api-key"]
        )