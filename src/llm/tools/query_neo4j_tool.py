from langchain_community.graphs import Neo4jGraph

class QueryNeo4jTool:
    def __init__(self, graph_client: Neo4jGraph):
        self.graph_client = graph_client

    def run(self, query: str) -> dict:
        try:
            result = self.graph_client.query(query)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
