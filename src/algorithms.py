import networkx as nx
from itertools import product
from typing import NamedTuple


def find_exact_mcis(G1, G2):
    return(find_mcis(G1, G2, find_exact_max_clique))


def find_mcis(G1, G2, max_clique_finder):
    H = modular_product(G1, G2)
    mcis_isomorphism = max_clique_finder(H)

    return(mcis_isomorphism)


def find_exact_max_clique(graph):
        max_clique = _max_clique_backtracking(graph,
                                              Clique(tuple(), 0),
                                              list(graph.nodes()),
                                              Clique(tuple(), 0))
        return max_clique


def _max_clique_backtracking(H, clique, candidates, max_clique):
    if(clique.size > max_clique.size):
        max_clique = Clique(clique.clique, clique.size)

    nodes_to_test = candidates.copy()
    for v in nodes_to_test:
        extends_clique = True
        meet_A_type = False
        for clique_vertex in clique.clique:
            if(not H.has_edge(v, clique_vertex)):
                extends_clique = False
                break
            edge_type = H.get_edge_data(v, clique_vertex, 'type')['type']
            if(edge_type == 'A'):
                meet_A_type = True

        if(not extends_clique):
            candidates.remove(v)
            continue

        if(not meet_A_type and clique.size > 0):
            continue

        candidates.remove(v)
        max_clique = _max_clique_backtracking(H,
                                              expand_clique(clique, v, 1),
                                              candidates.copy(),
                                              max_clique)

    return max_clique


def _node_product(G, H):
    for u, v in product(G, H):
        yield ((u, v), dict())


def modular_product(G, H):
    GH = nx.Graph()
    GH.add_nodes_from(_node_product(G, H))
    for (x1, y1) in GH.nodes:
        for (x2, y2) in GH.nodes:
            if(x1 == x2 or y1 == y2):
                continue

            if(G.has_edge(x1, x2) and H.has_edge(y1, y2)):
                GH.add_edge((x1, y1), (x2, y2), type='A')
            elif(not G.has_edge(x1, x2) and not H.has_edge(y1, y2)):
                GH.add_edge((x1, y1), (x2, y2), type='B')

    return GH


def expand_clique(clique, vertex, size_difference):
    return Clique(clique.clique + (vertex,),
                  clique.size + size_difference)


class Clique(NamedTuple):
    clique: tuple
    size: int
