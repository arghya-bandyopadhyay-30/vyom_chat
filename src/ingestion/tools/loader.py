import csv
import requests

from src.ingestion.models.edges import Edge
from src.ingestion.models.ingestion import Ingestion
from src.ingestion.models.nodes import Node
from src.ingestion.utiliies.uuid_provider import UUIDProvider


class Loader:
    """
    Loader class to process data, create nodes and edges, and populate a Neo4j graph database.
    Handles skill extraction and mapping relationships based on node types.
    """
    def __init__(self, ingestion_config: Ingestion):
        self.urls = ingestion_config.urls
        self.graph_client = ingestion_config.graph_client
        self.person_node = None
        self.unique_skills = set()
        self.skill_nodes = {}
        self.relationship_mapping = {
            "education": "HAS_EDUCATION",
            "experience": "HAS_EXPERIENCE",
            "language": "SPEAKS",
            "honour_and_awards": "RECEIVED_AWARD",
            "recommendation": "HAS_RECOMMENDATION",
            "blog": "AUTHORED",
            "projects": "WORKED_ON_PROJECT",
            "certifications": "HAS_CERTIFICATION",
            "skills": "IS_SKILLED",
        }

    async def run(self):
        """
        Main method to process data and populate the graph.
        """
        nodes, edges = self.process_data()
        self.graph_client.populate_graph(nodes, edges)

    def __extract_skills(self, skills_field: str) -> list[str]:
        """
        Extracts individual skills from a skills field, assuming skills are separated by '|'.
        """
        return [skill.strip() for skill in skills_field.split("|") if skill.strip()]

    def __create_nodes(self, node_type: str, row: dict) -> Node:
        """
        Creates a Node object with a unique ID and node type.
        """
        skills = self.__extract_skills(row.get("skills", ""))
        self.unique_skills.update(skills)
        node = Node(id=UUIDProvider.generate_id(), node_type=node_type, parameters=row)

        if node_type == "person" and not self.person_node:
            self.person_node = node

        return node

    def __create_edges(self, nodes: list[Node]) -> list[Edge]:
        """
        Create edges from each person node to other nodes based on the node_type.
        """
        if not self.person_node:
            raise ValueError("Person node not found. Ensure person data is present.")

        edges = []

        for node in nodes:
            if node.node_type == "person":
                continue

            relationship_type = self.relationship_mapping.get(node.node_type)
            edges.append(Edge(
                from_node=self.person_node,
                to_node=node,
                relationship_type=relationship_type
            ))

            if node.node_type in {"experience", "projects", "certifications"}:
                edges.extend(self.__create_skill_edges(node))

        return edges

    def __create_skill_nodes(self) -> list[Node]:
        """
         Creates nodes for unique skills extracted from data.
        """
        for skill in self.unique_skills:
            if skill not in self.skill_nodes:
                skill_node = self.__create_nodes("skills", {'name': skill})
                self.skill_nodes[skill] = skill_node

        return list(self.skill_nodes.values())

    def __create_skill_edges(self, node: Node) -> list[Edge]:
        """
        Creates edges between experience, project, or certification nodes and skill nodes.
        """
        skill_edges = []
        skills = self.__extract_skills(node.parameters.pop("skills", ""))

        for skill in skills:
            skill_node = self.skill_nodes.get(skill)
            if skill_node:
                skill_edges.append(
                    Edge(
                        from_node=node,
                        to_node=skill_node,
                        relationship_type="REQUIRED_SKILL"
                    )
                )

        return skill_edges

    def process_data(self) -> tuple[list[Node], list[Edge]]:
        """
        Processes data from URLs to create nodes and edges for the graph.
        """
        nodes = []

        for node_type, url in self.urls.items():
            csv_data = self.__fetch_csv_data(url)

            for row in csv_data:
                nodes.append(self.__create_nodes(node_type, row))

        nodes.extend(self.__create_skill_nodes())

        edges = self.__create_edges(nodes)

        return nodes, edges

    def __fetch_csv_data(self, url) -> list[dict[str, str]]:
        """
        Fetches CSV data from a URL and returns a list of dictionaries, where each
        dictionary represents a row with column names as keys.
        """
        response = requests.get(url)
        response.raise_for_status()

        decoded_content = response.content.decode("utf-8").splitlines()
        return list(csv.DictReader(decoded_content))
