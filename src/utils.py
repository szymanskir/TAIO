import networkx as nx
import numpy as np


def read_graph(filepath):
    """Creates a graph based on the content filepath.

    filepath -- filepath to a csv fiel containg the
    adjacency matrix
    """
    g_data = np.loadtxt(open(filepath, "rb"), delimiter=",")
    return nx.from_numpy_matrix(g_data)


def save_mccis(filename, clique):
    """Saves data from the clique into a file.

    Arguments:
    filename -- path to file in which the clique data
    should be saved

    clique - clique result given by a clique finding
    algorithm
    """
    np.savetxt(filename,
               np.transpose(np.asarray(clique)),
               fmt='%i',
               delimiter=',')
