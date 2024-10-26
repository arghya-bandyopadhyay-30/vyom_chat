import csv
import requests

from src.ingestion.models.edges import Edge
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

    def __create_edges(self, nodes: list[Node], person: Node) -> list[Edge]:
        """
        Create edges from each person node to other nodes based on the node_type.
        """
        edges = []
        relationship_mapping = {
            "education": "HAS_EDUCATION",
            "experience": "HAS_EXPERIENCE",
            "language": "SPEAKS",
            "honour_and_awards": "RECEIVED_AWARD",
            "recommendation": "HAS_RECOMMENDATION",
            "blog": "AUTHORED",
            "projects": "WORKED_ON_PROJECT",
            "certifications": "HAS_CERTIFICATION",
        }

        for node in nodes:
            if node.node_type == "person":
                continue

            relationship_type = relationship_mapping.get(node.node_type)
            edges.append(
                Edge(
                    from_node=person,
                    to_node=node,
                    relationship_type=relationship_type
                )
            )

        return edges

    def process_data(self):
        nodes = []
        person_node = None

        for node_type, url in self.urls.items():
            csv_data = self.__fetch_csv_data(url)

            for row in csv_data:
                node = self.__create_nodes(node_type, row)
                nodes.append(node)

                if node_type == "person":
                    person_node = node

        edges = self.__create_edges(nodes, person_node)

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
