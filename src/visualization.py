import networkx as nx
import matplotlib.pyplot as plt

from itertools import combinations


def draw_results(G1, G2, H, clique):
    """Draws the input graphs and their modular product with the
    found clique and common subgraphs highlighted.
    """
    g1_nodes = [g1_node for g1_node, _ in list(clique.vertices)]
    draw_graph_with_induced_subgraph(G1, g1_nodes, 'G1')

    g2_nodes = [g2_node for _, g2_node in list(clique.vertices)]
    draw_graph_with_induced_subgraph(G2, g2_nodes, 'G2')

    draw_graph_with_induced_subgraph(H, list(clique.vertices),
                                     'Modular Product')


def draw_graph_with_induced_subgraph(graph, nodes=None, plot_title=None):
    """Draws a single graph with the induced subgraph highlighted."""
    nodes = nodes if nodes else list()
    fig = plt.figure()
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

    return fig


def save_graph_plot(graph, output_file, nodes=None, plot_title=None):
    """Saves the drawn plot graph."""
    fig = draw_graph_with_induced_subgraph(graph, nodes, plot_title)
    fig.savefig(output_file, format='pdf')


def find_induces_edges(graph, nodes):
    """Find all edges connecting the given nodes in the given graph.

    Returns
    ----------
    List of edges connecting the given nodes.
    """
    induced_edges = list()
    for x, y in combinations(nodes, 2):
        edge = graph.get_edge_data(x, y)
        if edge:
            induced_edges.append((x, y))

    return induced_edges
