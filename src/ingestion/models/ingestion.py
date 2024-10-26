from langchain_community.graphs import Neo4jGraph

from src.ingestion.graph.graph_constructor import GraphClientBuilder
from src.ingestion.utiliies.csv_url import convert_to_csv_url


class Ingestion:
    """
    Class for managing data ingestion into a Neo4j graph database.
    Converts URLs to CSV format and initializes a Neo4j graph client.
    """
    def __init__(self, urls: dict, graph_client: Neo4jGraph):
        """
        Initializes Ingestion with URLs and a graph client instance.

        Parameters:
        - urls (dict): A dictionary mapping node types to their data source URLs.
        - graph_client (Neo4jGraph): The graph client for Neo4j interaction.
        """
        self.urls = {node_type: convert_to_csv_url(url) for node_type, url in urls.items()}
        self.graph_client = graph_client

    @classmethod
    def from_dict(cls, config: dict):
        """
        Creates an Ingestion instance from a configuration dictionary.

        Parameters:
        - config (dict): Configuration dictionary containing the database name and URLs.

        Returns:
        - Ingestion instance with converted URLs and initialized Neo4j client.

        Raises:
        - ValueError: If required 'db_name' or 'urls' fields are missing in the config.
        """
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