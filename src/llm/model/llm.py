from dataclasses import dataclass

@dataclass
class LLMConfig:
    provider: str
    api_key: str
    model: str
    base_url: str
    context_window: int

    @classmethod
    def from_dict(cls, config: dict):
        required_fields = ["provider", "api-key", "model", "base-url", "context-window"]
        for field in required_fields:
            if field not in config or not config[field]:
                raise ValueError(f"LLM configuration: '{field}' is required")

        return cls(
            model=config["model"],
            provider=config["provider"],
            base_url=config["base-url"],
            api_key=config["api-key"],
            context_window=config["context-window"]
        )