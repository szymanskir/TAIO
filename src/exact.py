import sys
import networkx as nx
import numpy as np
from itertools import product

current_max = 0
current_max_clique = list()


def max_clique(H, clique, candidates):
    global current_max
    global current_max_clique
    if(len(clique) > current_max):
        current_max = len(clique)
        current_max_clique = clique.copy()

    nodes_to_test = candidates.copy()
    for v in nodes_to_test:
        extendsClique = True
        meetAType = False
        for cliqueV in clique:
            if(not H.has_edge(v, cliqueV)):
                extendsClique = False
                break
            # print(str(v) + " " + str(cliqueV))
            edgeType = H.get_edge_data(v, cliqueV, 'type')['type']
            if(edgeType == 'A'):
                meetAType = True

        if(not extendsClique):
            candidates.remove(v)
            continue

        if(not meetAType and len(clique) > 0):
            continue

        candidates.remove(v)
        clique.append(v)
        max_clique(H, clique, candidates.copy())
        clique.remove(v)


def read_graph(filepath):
    g_data = np.loadtxt(open(filepath, "rb"), delimiter=",")
    return nx.from_numpy_matrix(g_data)


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


def print_isomorphism(clique):
    G1_iso = list()
    G2_iso = list()

    for (x, y) in clique:
        G1_iso.append(x)
        G2_iso.append(y)

    print(G1_iso)
    print(G2_iso)


G1 = read_graph("data/2a.csv")
G2 = read_graph("data/2b.csv")

H = modular_product(G1, G2)

max_clique(H, list(), list(H.nodes()))
print(current_max_clique)

print_isomorphism(current_max_clique)
