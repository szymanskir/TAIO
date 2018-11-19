import networkx as nx
import matplotlib.pyplot as plt

from itertools import combinations

fig_size = (6, 4)
output_format = '.pdf'


def draw_results(G1, G2, H, clique):
    """Draws the input graphs and their modular product with the
    found clique and common subgraphs highlighted.
    """
    g1_nodes = [g1_node for g1_node, _ in list(clique.vertices)]
    _draw_input_graph_(G1, g1_nodes, 'G1')

    g2_nodes = [g2_node for _, g2_node in list(clique.vertices)]
    _draw_input_graph_(G2, g2_nodes, 'G2')

    _draw_modular_graph_(H, list(clique.vertices),
                         'Modular Product')


def draw_and_save_results(G1, G2, H, clique, output_file="tmp"):
    """Saves the drawn plot graph."""
    g1_nodes = [g1_node for g1_node, _ in list(clique.vertices)]
    fig_g1 = _draw_input_graph_(G1, g1_nodes)
    fig_g1.set_size_inches(fig_size)
    fig_g1.savefig(f"{output_file}-g1{output_format}")

    g2_nodes = [g2_node for _, g2_node in list(clique.vertices)]
    fig_g2 = _draw_input_graph_(G2, g2_nodes)
    fig_g2.set_size_inches(fig_size)
    fig_g2.savefig(f"{output_file}-g2{output_format}")

    fig_h = _draw_modular_graph_(H, list(clique.vertices))
    fig_h.set_size_inches(10, 8)
    fig_h.savefig(f"{output_file}-h{output_format}")


def _draw_input_graph_(graph, nodes=None, plot_title=''):
    return _draw_graph_with_induced_subgraph_(
        graph, nodes, plot_title)


def _draw_modular_graph_(graph, nodes=None, plot_title=''):
    return _draw_graph_with_induced_subgraph_(
        graph, nodes, plot_title, marker_size=1100)


def _draw_graph_with_induced_subgraph_(graph, nodes=None, plot_title='', marker_size=500):
    """Draws a single graph with the induced subgraph highlighted."""
    nodes = nodes if nodes else list()
    fig = plt.figure()
    pos = nx.circular_layout(graph)
    induced_edges = find_induces_edges(graph, nodes)

    node_args = dict(node_color='w', edgecolors='k',
                     node_size=marker_size, linewidths=1.5)
    nx.draw_networkx_nodes(graph,
                           pos,
                           nodelist=set(graph.nodes)-set(nodes),
                           node_shape='s',
                           **node_args)
    nx.draw_networkx_nodes(graph,
                           pos,
                           nodelist=nodes,
                           node_shape='o',
                           **node_args)

    nx.draw_networkx_edges(graph,
                           pos,
                           edgelist=set(graph.edges)-set(induced_edges),
                           style='dashed')
    nx.draw_networkx_edges(graph,
                           pos,
                           edgelist=induced_edges,
                           style='solid')

    nx.draw_networkx_labels(graph, pos, font_size=14)

    plt.title(plot_title)
    plt.axis('off')
    fig.tight_layout()

    return fig


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
