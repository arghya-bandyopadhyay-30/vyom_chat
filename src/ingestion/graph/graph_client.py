from langchain_community.graphs import Neo4jGraph

from src.ingestion.models.edges import Edge
from src.ingestion.models.nodes import Node


class GraphClient:
    def __init__(self, url, username, password, db_name):
        self.graph = Neo4jGraph(
            url=url,
            username=username,
            password=password,
            database=db_name
        )

    def close(self):
        self.graph.close()

    def populate_graph(self, nodes: list[Node], edges: list[Edge]):
        self.__create_nodes(nodes)
        self.__create_edges(edges)

    def __create_nodes(self, nodes: list[Node]):
        return self.graph.query(
            """
            WITH $data AS batch
            UNWIND batch AS node
            MERGE (k {id: node.id}) 
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
                        "id": node.id,
                        "node_type": node.node_type,
                        "parameters": node.parameters
                    }
                    for node in nodes
                ]
            }
        )

    def __create_edges(self, edges: list[Edge]):
        if not edges:
            return

        self.graph.query(
            """
            WITH $data AS batch
            UNWIND batch AS edge
            MATCH (from {id: edge.from_node_id})  
            MATCH (to {id: edge.to_node_id})
            CALL apoc.create.relationship(from, edge.relationship_type, {}, to) YIELD rel
            RETURN rel
            """,
            {
                "data": [
                    {
                        "from_node_id": edge.from_node.id,
                        "to_node_id": edge.to_node.id,
                        "relationship_type": edge.relationship_type,
                    }
                    for edge in edges
                ]
            },
        )

    def delete_all(self):
        self.graph.query(
            """
                MATCH (n) DETACH DELETE n
            """
        )