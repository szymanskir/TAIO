import networkx as nx
import logging

from math import ceil, floor


def generate_test_case(graph_type, vertex_number, edge_probability):
    """Generates a graph with vertex_number vertices
    of the given type.
    """
    logging.debug(f'Generating {graph_type} graph with {vertex_number} vertices.')
    edge_probability = 0.8 if edge_probability is None else edge_probability
    graph_generator = _graph_generator_factory(graph_type)

    if graph_type == 'dense':
        result = graph_generator(vertex_number, edge_probability)
    elif graph_type == 'sparse':
        result = graph_generator(vertex_number, edge_probability)
    elif graph_type == 'random':
        result = graph_generator(vertex_number, edge_probability)
    else:
        result = graph_generator(vertex_number)

    return result


def _graph_generator_factory(graph_type):
    graph_generators = {
        'path': nx.path_graph,
        'complete': nx.complete_graph,
        'cycle': nx.cycle_graph,
        'tree': nx.random_tree,
        'dense': _generate_random_connected_graph,
        'sparse': _generate_random_connected_graph,
        'random': _generate_random_connected_graph,
        'bipartite': _generate_random_connected_bipartite_graph
    }

    return graph_generators[graph_type]


def _generate_random_connected_bipartite_graph(vertex_number):
    while True:
        G = nx.algorithms.bipartite.generators.complete_bipartite_graph(
            ceil(vertex_number/2),
            floor(vertex_number/2))
        if nx.is_connected(G):
            break

    return G


def _generate_random_connected_graph(vertex_number, edge_probability):
    G = nx.fast_gnp_random_graph(vertex_number, edge_probability)
    while not nx.is_connected(G):
        G = nx.fast_gnp_random_graph(vertex_number, edge_probability)

    return G
