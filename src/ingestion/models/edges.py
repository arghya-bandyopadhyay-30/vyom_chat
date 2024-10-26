from src.ingestion.models.nodes import Node

class Edge:
    def __init__(self, from_node: Node, to_node: Node, relationship_type: str):
        self.from_node = from_node
        self.to_node = to_node
        self.relationship_type = relationship_type

    def __repr__(self):
        return (f"Edge(from={self.from_node.node_type}, "
                f"to={self.to_node.node_type}, "
                f"relationship_type={self.relationship_type})")