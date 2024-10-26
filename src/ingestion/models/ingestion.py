import os

from langchain_community.graphs import Neo4jGraph
from src.ingestion.graph.graph_constructor import GraphClientBuilder
from src.ingestion.models.edges import Edge
from src.ingestion.models.nodes import Node
from src.ingestion.utiliies.csv_url import convert_to_csv_url


class Ingestion:
    def __init__(self, urls: dict, graph_client: Neo4jGraph):
        self.urls = {node_type: convert_to_csv_url(url) for node_type, url in urls.items()}
        self.graph_client = graph_client

    @classmethod
    def from_dict(cls, config: dict):
        if "db_name" not in config or not config["db_name"]:
            raise ValueError("Ingestion db_name is required")

        if "urls" not in config or not config["urls"]:
            raise ValueError("Ingestion urls are required")

        graph_client_builder = GraphClientBuilder(config["db_name"])
        graph_client = graph_client_builder.client()

        return cls(
            urls=config["urls"],
            graph_client=graph_client,
        )

    def test_populate_graph(self):
        person = Node("1", "Person", {"id": "1", "name": "Alice", "age": 30})
        education = Node("2","Education", {"id": "2", "institute": "TMSL", "dept": "computer"})
        educated_at_edge = Edge(from_node="1", to_node="2", relationship_type="EDUCATED_AT")

        test_nodes = [person, education]
        test_edges = [educated_at_edge]

        self.graph_client.populate_graph(test_nodes, test_edges)
        # self.graph_client.delete_all()
        self.graph_client.close()