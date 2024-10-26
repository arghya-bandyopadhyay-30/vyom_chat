import numpy as np
from neo4j import GraphDatabase

from src.ingestion.models.edges import Edge
from src.ingestion.models.nodes import Node


class GraphClient:
    def __init__(self, url, auth, db_name):
        self.driver = GraphDatabase.driver(url, auth=auth)
        self.db_name = db_name

    def close(self):
        self.driver.close()

    def populate_graph(self, nodes: list[Node], edges: list[Edge]):
        self.__create_nodes(nodes)
        self.__create_edges(edges)

    def __create_nodes(self, nodes: list[Node]):
        """
        Creates nodes in the Neo4j database using the Node objects provided.
        Uses APOC to dynamically set labels and properties.
        """
        return self.driver.execute_query(
            """
            WITH $data AS batch
            UNWIND batch AS node
            MERGE (k {id: node.id})  // Use `node.id` as the unique identifier
            WITH k, node
            CALL apoc.create.addLabels(k, [node.node_type]) YIELD node AS labeledNode
            WITH labeledNode, node
            UNWIND keys(node.parameters) AS key
            CALL apoc.create.setProperty(labeledNode, key, node.parameters[key]) YIELD node AS updatedNode
            RETURN updatedNode
            """,
            {
                "data": [
                    {
                        "id": node.id,  # Use `id` directly from the Node object
                        "node_type": node.node_type,
                        "parameters": node.parameters  # Other properties to be set
                    }
                    for node in nodes
                ]
            },
            database_=self.db_name,
        )

    def __create_edges(self, edges: list[Edge]):
        """
        Creates edges in the Neo4j database using the Edge objects provided.
        """
        if not edges:
            return

        self.driver.execute_query(
            """
            WITH $data AS batch
            UNWIND batch AS edge
            MATCH (from {id: edge.from_node})  
            MATCH (to {id: edge.to_node})
            CALL apoc.create.relationship(from, edge.relationship_type, {}, to) YIELD rel
            RETURN rel
            """,
            {
                "data": [
                    {
                        "from_node": edge.from_node,  # Use `from_node` and `to_node` as IDs
                        "to_node": edge.to_node,
                        "relationship_type": edge.relationship_type,
                    }
                    for edge in edges
                ]
            },
            database_=self.db_name,
        )

    def delete_all(self):
        """
        Deletes all nodes and relationships in the database.
        """
        self.driver.execute_query(
            """
                MATCH (n) DETACH DELETE n
            """,
            database_=self.db_name,
        )