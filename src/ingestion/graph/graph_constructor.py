import os

from src.ingestion.graph.graph_client import GraphClient

class GraphClientBuilder:
    def __init__(self, db_name = "neo4j"):
        self.neo4j_url = os.getenv("NEO4J_URI")
        self.neo4j_username = os.getenv("NEO4J_USERNAME")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.auth = (self.neo4j_username, self.neo4j_password)
        self.db_name = db_name

    def client(self):
        return GraphClient(
            url=self.neo4j_url,
            auth=self.auth,
            db_name=self.db_name
        )
