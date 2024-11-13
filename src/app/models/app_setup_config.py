from langchain_community.graphs import Neo4jGraph

from src.graph.graph_constructor import GraphClientBuilder


class AppSetupConfig:
    def __init__(self, page_title: str, page_icon: str, title: str, subtitle: str, graph_client: Neo4jGraph):
        self.page_title = page_title
        self.page_icon = page_icon
        self.title = title
        self.subtitle = subtitle
        self.graph_client = graph_client

    @classmethod
    def from_dict(cls, config: dict):
        required_fields = ["title", "subtitle", "db_name"]
        for field in required_fields:
            if field not in config or not config[field]:
                raise ValueError(f"App configuration: '{field}' is required")

        graph_client_builder = GraphClientBuilder(config["db_name"])
        graph_client = graph_client_builder.client()

        return cls(
            page_title=config.get("page_title", "Vyom"),
            page_icon=config.get("page_icon", "🧘‍♂️"),
            title=config["title"],
            subtitle=config["subtitle"],
            graph_client=graph_client,
        )
