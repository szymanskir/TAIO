import sys
import matplotlib.pyplot as plt
import networkx as nx

current_max = 0
current_max_clique = list()


def max_clique(clique, candidates):
    global current_max
    global current_max_clique
    if(len(clique) > current_max):
        current_max = len(clique)
        current_max_clique = clique.copy()

    if(len(candidates) == 0 or len(clique) == G.number_of_nodes()):
        return

    nodes_to_test = candidates.copy()
    while(len(nodes_to_test) > 0):
        v = nodes_to_test.pop()

        extendsClique = True
        meetAType = False
        for cliqueV in clique:
            if(not G.has_edge(v, cliqueV)):
                extendsClique = False
                break
            # print(str(v) + " " + str(cliqueV))
            edgeType = G.get_edge_data(v, cliqueV, 'type')['type']
            if(edgeType == 'A'):
                meetAType = True

        if(not extendsClique):
            candidates.remove(v)
            continue

        if(not meetAType and len(clique) > 0):
            continue

        candidates.remove(v)
        clique.append(v)
        max_clique(clique, candidates.copy())
        clique.remove(v)


G = nx.Graph()
edges = [
    (0, 1, {'type': 'B'}),
    (0, 2, {'type': 'A'}),
    (0, 3, {'type': 'B'}),
    (0, 4, {'type': 'A'}),
    (1, 2, {'type': 'B'}),
    (1, 3, {'type': 'B'}),
    (2, 3, {'type': 'A'}),
    (2, 4, {'type': 'B'})
]

G.add_edges_from(edges)
# print(G.get_edge_data(2, 1, 'type')['type'])
# edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
# nx.draw_circular(G, with_labels=True)
# plt.show()

clique = nx.find_cliques(G)
print(next(clique))

max_clique(list(), list(G.nodes()))
print(current_max_clique)

# nx.draw_circular(clique, with_labels=True)
# plt.show()
