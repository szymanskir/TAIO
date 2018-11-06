import networkx as nx
import numpy as np


def save_graph(graph, output_file):
    """Saves the adjacency matrix of a given graph in csv format.

    It is assumed that nodes are labeled from 0 to n-1.

    Parameters
    ----------
    graph : networkx graph


    filename : filepath
        Path to file contaning in which the adjacency matrix will
        be saved.
    """
    n = graph.number_of_nodes()
    adjacency_matrix = np.zeros((n, n))

    for x, y in graph.edges:
        adjacency_matrix[x, y] = 1
        adjacency_matrix[y, x] = 1

    np.savetxt(output_file,
               adjacency_matrix,
               fmt='%i',
               delimiter=',')


def read_graph(filepath):
    """Creates a graph based on the content filepath.

    Parameters
    ----------
    filename : filepath
        Path to file contaning an adjacency matrix.
    """
    g_data = np.loadtxt(open(filepath, "rb"), delimiter=",")
    return nx.from_numpy_matrix(g_data)


def save_mccis(filename, clique):
    """Saves data from the clique into a file.

    Parameters
    ----------
    filename : filepath
        Path to file in which the clique data should be saved

    clique : list of vertices.
        Clique result given by a clique finding algorithm
    """
    np.savetxt(filename,
               np.transpose(np.asarray(clique)),
               fmt='%i',
               delimiter=',')
