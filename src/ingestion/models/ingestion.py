from langchain_community.graphs import Neo4jGraph

from src.graph.graph_constructor import GraphClientBuilder
from src.ingestion.utiliies.csv_url import convert_to_csv_url

class Ingestion:
    def __init__(self, urls: dict, graph_client: Neo4jGraph):
        self.urls = {node_type: convert_to_csv_url(url) for node_type, url in urls.items()}
        self.graph_client = graph_client

    @classmethod
    def from_dict(cls, config: dict):
        if "db_name" not in config or not config["db_name"]:
            raise ValueError("Ingestion configuration: db_name is required")

        if "urls" not in config or not config["urls"]:
            raise ValueError("Ingestion configuration: urls are required")

        graph_client_builder = GraphClientBuilder(config["db_name"])
        graph_client = graph_client_builder.client()

        graph_client.delete_all()

        return cls(
            urls=config["urls"],
            graph_client=graph_client,
        )