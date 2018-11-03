import networkx as nx
import numpy as np


def read_graph(filepath):
    g_data = np.loadtxt(open(filepath, "rb"), delimiter=",")
    return nx.from_numpy_matrix(g_data)


def save_mccis(filename, clique):
    np.savetxt(filename,
               np.transpose(np.asarray(clique)),
               fmt='%i',
               delimiter=',')


def print_isomorphism(clique):
    G1_iso = list()
    G2_iso = list()

    for (x, y) in clique:
        G1_iso.append(x)
        G2_iso.append(y)

    print(G1_iso)
    print(G2_iso)
