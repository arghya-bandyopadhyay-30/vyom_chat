from typing import Dict, Any
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class Node:
    id: str
    node_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)