from dataclasses import dataclass

@dataclass
class Settings:
    base_url: str
    model_name: str
    api_key: str
    batch_size: int
    rpm: int
    tpm: int

    @classmethod
    def from_dict(cls, config: dict):
        required_fields = ["base-url", "model-name", "api-key", "batch-size", "rpm", "tpm"]
        for field in required_fields:
            if field not in config or not config[field]:
                raise ValueError(f"Embedding setting '{field}' is required")

        return cls(
            base_url=config["base-url"],
            model_name=config["model-name"],
            api_key=config["api-key"],
            batch_size=config["batch-size"],
            rpm=config["rpm"],
            tpm=config["tpm"]
        )