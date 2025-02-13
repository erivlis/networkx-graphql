import networkx as nx
import strawberry
from graphinate import GraphModel, GraphType, graphql
from graphinate.builders import GraphQLBuilder
from graphinate.typing import Extractor


def graph_type(graph: nx.Graph) -> GraphType:
    if graph.is_directed() and graph.is_multigraph():
        return GraphType.MultiDiGraph
    elif graph.is_directed():
        return GraphType.MultiGraph
    elif graph.is_multigraph():
        return GraphType.MultiDiGraph.MultiGraph
    else:
        return GraphType.Graph


def schema(graph: nx.Graph, node_type_extractor: Extractor | None = None) -> strawberry.Schema:
    graph_model = GraphModel(name=graph.name)

    node_type_extractor = node_type_extractor if callable(node_type_extractor) else 'node'

    @graph_model.node(node_type_extractor)
    def nodes():
        yield from graph.nodes

    @graph_model.edge('edge')
    def edges():
        for edge in graph.edges:
            yield {'source': edge[0], 'target': edge[1]}

    graphql_builder = GraphQLBuilder(graph_model, graph_type=graph_type(graph))

    return graphql_builder.build()


def run(schema: strawberry.Schema, port: 8073) -> dict:
    return graphql(schema, port)
