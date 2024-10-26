import csv
import requests

from src.ingestion.models.ingestion import Ingestion
from src.ingestion.models.nodes import Node
from src.ingestion.utiliies.uuid_provider import UUIDProvider


class Loader:
    def __init__(self, ingestion_config: Ingestion):
        self.urls = ingestion_config.urls
        self.graph_client = ingestion_config.graph_client

    async def run(self):
        nodes, edges = self.process_data()

        self.graph_client.populate_graph(nodes, edges)

    def __create_nodes(self, node_type: str, row: dict) -> Node:
        return Node(
            id = UUIDProvider.generate_id(),
            node_type = node_type,
            parameters = row,
        )

    def process_data(self):
        nodes = []
        edges = []

        for node_type, url in self.urls.items():
            csv_data = self.__fetch_csv_data(url)

            for row in csv_data:
                nodes.append(self.__create_nodes(node_type, row))

        return nodes, edges

    def __fetch_csv_data(self, url):
        """
        Fetches CSV data from a URL and returns a list of dictionaries, where each
        dictionary represents a row with column names as keys.
        """
        response = requests.get(url)
        response.raise_for_status()

        decoded_content = response.content.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_content)

        return reader
