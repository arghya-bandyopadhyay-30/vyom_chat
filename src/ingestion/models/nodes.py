class Node:
    def __init__(self, id: str, node_type: str, parameters: dict):
        self.id = id
        self.node_type = node_type
        self.parameters = parameters

    def __repr__(self):
        return f"Node(type={self.node_type}, parameters={self.parameters})"