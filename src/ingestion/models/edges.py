from pydantic.dataclasses import dataclass
from src.ingestion.models.nodes import Node

@dataclass
class Edge:
    from_node: Node
    to_node: Node
    relationship_type: str