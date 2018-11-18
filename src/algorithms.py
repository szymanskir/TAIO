import networkx as nx
import logging
import matplotlib.pyplot as plt

from itertools import product
from collections import deque
from typing import NamedTuple
from enum import Enum
from math import log, ceil

from .utils import read_graph, save_mccis
from .visualization import draw_results


def find_mccis(graph_csv1, graph_csv2, output_file, size_criterion, exact, visualize):
    """Finds the maximal common connected subgraph of two graphs described by
    separate csv files containing corresponding adjacency matrices.

    Parameters
    ----------
    graph_csv1, graph_csv2 : filepaths.
        Csv files contaning the adjacency matrices of the input graphs.

    output_file : filepath
        Path to the file in which the result should be saved.

    size_criterion : SizeCriterion value
        The considered size criterion:
            * highest amount of vertices
            * highest amount of vertices and edges

    exact : bool
        Should the exact or the approximation algorithm be used.

    visualize : bool
        Should the results be displayed.
    """
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
        draw_results(G1, G2, modular_product(G1, G2), mccis)
        plt.show()


def find_mccis_factory(exact):
    """Creates a function calculating the maximal common connected subgraph
    based on arguments.
    """
    if exact:
        return create_find_mccis_function(find_exact_max_clique)
    else:
        return create_find_mccis_function(find_approx_max_clique)


def create_find_mccis_function(max_clique_finder):
    """Creates a function that will find the maximal
    common connected subgraph using the given max clique
    finding function.

    Parameters
    ----------
    max_clique_finder : function
        Function that finds the maximal clique in a given graph.

    Returns
    ----------
    Function that will find the maximal common connected subgraph
    of two graphs using the modular product.
    """
    def find_mccis(G1, G2, size_criterion):
        # validate criterion
        if not hasattr(SizeCriterion, size_criterion):
            raise ValueError(f'{size_criterion} is not a valid size criterion')

        H = modular_product(G1, G2)
        mccis_isomorphism = max_clique_finder(H, size_criterion)

        return(mccis_isomorphism)

    return find_mccis


def find_approx_max_clique(H, size_criterion):
    """Finds the maximal clique using an approximation algorithm.

    Parameters
    ----------
    H : networkx graph.
        Graph in which the maximal clique will be sought.

    size_criterion: SizeCriterion value
        The considered size criterion:
            * highest amount of vertices
            * highest amount of vertices and edges

    Returns
    ----------
    List of vertices belonging the maximal clique.
    """
    k = ceil(log(len(H.nodes), 2))

    visited = set()
    not_yet_visited = list(H.nodes)
    subgraphs = list()

    while (len(not_yet_visited) > 0):
        start = not_yet_visited[0]
        now_visited = _bfs_(H, start, visited, k)
        visited |= now_visited

        for v in now_visited:
            not_yet_visited.remove(v)

        if len(now_visited) > 0:
            subgraphs.append(list(now_visited))

    max_clique = Clique()
    for subgraph in subgraphs:
        clique = find_exact_max_clique(H.subgraph(subgraph), size_criterion)
        if(clique.size > max_clique.size):
            max_clique = clique

    return max_clique


def _bfs_(G, start_vertex, visited, k):
    """Performs BFS along A-type edges up till k vertices are visited.

    Parameters
    ----------
    G : networkx graph
        Graph in which BFS will be performed.

    start_vertex : int
        Vertex from which the BFS will start.

    visited : list of int
        List of already visited vertices.

    k : int
        Specifies how many vertices that can be visited.

    Returns
    ---------
    List of nodes visited during the BFS.
    """
    queue = deque([start_vertex])
    visited_now = set([start_vertex])
    while queue:
        vertex = queue.popleft()
        for neighbor, edge_attr in G.adj[vertex].items():
            if edge_attr['type'] == 'A' and neighbor not in visited:
                visited.add(neighbor)
                visited_now.add(neighbor)
                queue.append(neighbor)
                if (len(visited_now) == k):
                    return visited_now

    return visited_now


def find_exact_max_clique(graph, size_criterion):
    """Finds the exact maximal clique in the graph

    Parameters
    ----------

    graph: networkx graph
        Graph in which the maximal clique will be found.

    size_criterion: SizeCriterion value
        The considered size criterion:
            * highest amount of vertices
            * highest amount of vertices and edges
    """
    def _max_clique_backtracking(H, clique, candidates, max_clique, size_criterion):
        """ Max clique backtracking function.

        Parameters
        ----------
        H : networkx graph
            Graph in which the maximal clique is sought.

        clique : list of vertices
            The current clique being considered.

        candidates : list of vertices
            Vertices that are considered to be added to the clique.

        max_clique : list of vertices
            The biggest clique found until now.

        size_criterion: SizeCriterion value
            The considered size criterion:
                * highest amount of vertices
                * highest amount of vertices and edges


        Returns
        ----------
        Maximal clique found.
        """
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
                    expand_clique(clique,
                                  candidate,
                                  edge_size_increase,
                                  size_criterion),
                    candidates.copy(),
                    max_clique,
                    size_criterion
                )

        return max_clique

    max_clique = _max_clique_backtracking(graph,
                                          Clique(),
                                          list(graph.nodes()),
                                          Clique(),
                                          size_criterion)
    return max_clique


def _node_product(G, H):
    """Calculates the node Cartesian product of G and H.
    """
    for u, candidate in product(G, H):
        yield ((u, candidate), dict())


def modular_product(G, H):
    """Calculates the graph modular product of G and H.

    Arguments:
    G, H - input graphs.
    """
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


def expand_clique(clique, vertex, edge_increase, size_criterion):
    """Updates the clique vertices and size accordingly."""
    if SizeCriterion[size_criterion] == SizeCriterion.Vertices:
        return Clique(clique.vertices + (vertex,),
                      clique.size + 1)
    elif SizeCriterion[size_criterion] == SizeCriterion.VerticesAndEdges:
        return Clique(clique.vertices + (vertex,),
                      clique.size + 1 + edge_increase)


class Clique(NamedTuple):
    """Class representing a clique."""
    vertices: tuple = tuple()
    size: int = 0


class SizeCriterion(Enum):
    """Class representing size measure criteria."""
    Vertices = 1
    VerticesAndEdges = 2
