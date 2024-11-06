from dataclasses import dataclass

@dataclass
class LLMConfig:
    provider: str
    api_key: str
    model: str

    @classmethod
    def from_dict(cls, config: dict):
        required_fields = ["provider", "api-key", "model"]
        for field in required_fields:
            if field not in config or not config[field]:
                raise ValueError(f"LLM configuration: '{field}' is required")

        return cls(
            model=config["model"],
            provider=config["provider"],
            api_key=config["api-key"],
        )