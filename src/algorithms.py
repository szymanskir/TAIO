import networkx as nx
import logging
import matplotlib.pyplot as plt

from itertools import product, combinations
from typing import NamedTuple
from enum import Enum
from math import log, ceil

from .utils import read_graph, save_mccis


def find_mccis(graph_csv1, graph_csv2, output_file, size_criterion, exact, visualize):
    logger = logging.getLogger('main')

    logger.info(f'Reading data from {graph_csv1} and {graph_csv2}...')
    G1 = read_graph(graph_csv1)
    G2 = read_graph(graph_csv2)

    logger.info('Calculating maximal mccis...')
    find_mccis = find_mccis_factory(exact)
    mccis = find_mccis(G1, G2, size_criterion)

    logger.info(f'Saving results to {output_file}...')
    save_mccis(output_file, mccis.vertices)

    if visualize:
        draw_results(G1, G2, mccis)
        plt.show()


def find_mccis_factory(exact):
    if exact:
        return create_find_mccis_function(find_exact_max_clique)
    else:
        return create_find_mccis_function(find_approx_max_clique)


def create_find_mccis_function(max_clique_finder):
    def find_mccis(G1, G2, size_criterion):
        # validate criterion
        if not hasattr(SizeCriterion, size_criterion):
            raise ValueError(f'{size_criterion} is not a valid size criterion')

        H = modular_product(G1, G2)
        mccis_isomorphism = max_clique_finder(H, size_criterion)

        return(mccis_isomorphism)

    return find_mccis


def find_approx_max_clique(H, size_criterion):
    k = ceil(log(len(H.nodes), 2))

    visited = set()
    not_yet_visited = set(H.nodes)
    subgraphs = list()

    while (len(not_yet_visited) > 0):
        now_visited = _bfs_(H, not_yet_visited.pop(), visited, k)
        visited |= now_visited
        not_yet_visited -= now_visited
        if len(now_visited) > 0:
            subgraphs.append(list(now_visited))

    max_clique = Clique()
    for subgraph in subgraphs:
        clique = _max_clique_backtracking(H,
                                          Clique(),
                                          subgraph,
                                          Clique(),
                                          size_criterion)
        if(clique.size > max_clique.size):
            max_clique = clique

    return max_clique


def _bfs_(G, start_vertex, visited, k):
    queue = [start_vertex]
    visited_now = set()
    while queue:
        vertex = queue.pop(0)
        for neighbor, edge_attr in G.adj[vertex].items():
            if edge_attr['type'] == 'A' and neighbor not in visited:
                visited.add(neighbor)
                visited_now.add(neighbor)
                queue.append(neighbor)
                if (len(visited_now) == k):
                    return visited_now

    return visited_now


def find_exact_max_clique(graph, size_criterion):
    max_clique = _max_clique_backtracking(graph,
                                          Clique(),
                                          list(graph.nodes()),
                                          Clique(),
                                          size_criterion)
    return max_clique


def _max_clique_backtracking(H, clique, candidates, max_clique, size_criterion):
    if(clique.size > max_clique.size):
        max_clique = clique

    nodes_to_test = candidates.copy()
    for candidate in nodes_to_test:
        edge_size_increase = 0
        extends_clique = True
        meet_A_type = False
        for clique_vertex in clique.vertices:
            edge = H.get_edge_data(candidate, clique_vertex)
            if not edge:
                extends_clique = False
                break
            elif edge['type'] == 'A':
                edge_size_increase += 1
                meet_A_type = True

        if not meet_A_type and clique.size > 0:
            continue

        candidates.remove(candidate)

        if extends_clique:
            max_clique = _max_clique_backtracking(
                H,
                expand_clique(clique, candidate,
                              edge_size_increase, size_criterion),
                candidates.copy(),
                max_clique,
                size_criterion
            )

    return max_clique


def _node_product(G, H):
    for u, candidate in product(G, H):
        yield ((u, candidate), dict())


def modular_product(G, H):
    GH = nx.Graph()
    GH.add_nodes_from(_node_product(G, H))
    for (x1, y1) in GH.nodes:
        for (x2, y2) in GH.nodes:
            if(x1 == x2 or y1 == y2):
                continue

            if G.has_edge(x1, x2) and H.has_edge(y1, y2):
                GH.add_edge((x1, y1), (x2, y2), type='A')
            elif not G.has_edge(x1, x2) and not H.has_edge(y1, y2):
                GH.add_edge((x1, y1), (x2, y2), type='B')

    return GH


class Clique(NamedTuple):
    vertices: tuple = tuple()
    size: int = 0


def expand_clique(clique, vertex, edge_increase, size_criterion):
    if SizeCriterion[size_criterion] == SizeCriterion.Vertices:
        return Clique(clique.vertices + (vertex,),
                      clique.size + 1)
    elif SizeCriterion[size_criterion] == SizeCriterion.VerticesAndEdges:
        return Clique(clique.vertices + (vertex,),
                      clique.size + 1 + edge_increase)


class SizeCriterion(Enum):
    Vertices = 1
    VerticesAndEdges = 2


def draw_results(G1, G2, clique):

    plt.subplot(221)
    g1_nodes = [g1_node for g1_node, _ in list(clique.vertices)]
    draw_graph_with_induced_subgraph(G1, g1_nodes, 'G1')

    plt.subplot(222)
    g2_nodes = [g2_node for _, g2_node in list(clique.vertices)]
    print(g2_nodes)
    draw_graph_with_induced_subgraph(G2, g2_nodes, 'G2')

    plt.subplot(223)
    H = modular_product(G1, G2)
    draw_graph_with_induced_subgraph(H, list(clique.vertices),
                                     'Modular Product')


def draw_graph_with_induced_subgraph(graph, nodes, plot_title):
    pos = nx.spring_layout(graph)
    induced_edges = find_induces_edges(graph, nodes)

    nx.draw_networkx(graph, pos, with_labels=True)
    nx.draw_networkx_nodes(graph,
                           pos,
                           nodelist=nodes,
                           node_size=1200,
                           node_color='skyblue')
    nx.draw_networkx_edges(graph,
                           pos,
                           edgelist=induced_edges,
                           edge_color='violet',
                           width=5)
    plt.title(plot_title)


def find_induces_edges(graph, nodes):
    induced_edges = list()
    for x, y in combinations(nodes, 2):
        edge = graph.get_edge_data(x, y)
        if edge:
            induced_edges.append((x, y))

    return induced_edges
