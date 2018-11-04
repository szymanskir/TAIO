import networkx as nx
import matplotlib.pyplot as plt

from itertools import combinations


def draw_graph_with_induced_subgraph(graph, nodes=list(), plot_title=None):
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


def save_graph_plot(graph, output_file, nodes=list(), plot_title=None):
    fig = draw_graph_with_induced_subgraph(graph)
    fig.savefig(output_file, format='pdf')


def find_induces_edges(graph, nodes):
    induced_edges = list()
    for x, y in combinations(nodes, 2):
        edge = graph.get_edge_data(x, y)
        if edge:
            induced_edges.append((x, y))

    return induced_edges
