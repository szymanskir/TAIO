import networkx as nx

from src.utils import save_graph

G1 = nx.Graph()
G1.add_edge(0, 1)
save_graph(G1, 'g1.txt')
