import networkx as nx
import matplotlib.pyplot as plt
from edges import edges, weighted_nodes, source_node

Gr1 = nx.Graph()

draw_all = True

Gr1.add_edges_from(edges)

all_edges = [edge for edge in Gr1.edges()]

green_edges = [edge for edge in nx.dfs_edges(Gr1, 'ТК-35/4')]  # подключенный подграф
black_edges = [edge for edge in Gr1.edges() if edge not in green_edges]  # неподключенный подграф

edge_colours = ['black' if not edge in green_edges else 'green'
                for edge in Gr1.edges()]

nodeset = set()
for n1, n2 in green_edges:
    nodeset.add(n1)
    nodeset.add(n2)

G = nx.Graph()

# рисуем связи


G.add_edges_from(all_edges)
pos = nx.planar_layout(G)

nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='r', arrows=False)

nx.draw_networkx_nodes(G, pos, node_size=10, margins=0)

nx.draw_networkx_labels(G, pos, font_size=10)

plt.show()


plt.clf()
G = nx.Graph()
G.add_edges_from(green_edges)
pos = nx.planar_layout(G, center=(10, 10), scale=10)

nx.draw_networkx_nodes(G, pos, nodelist=list(nodeset), node_size=10, margins=0)  # рисуем все ноды

nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='g', arrows=False)

nx.draw_networkx_labels(G, pos, labels={k: k for k in nodeset}, font_size=10)  # рисуем все подписи

plt.show()

print(G.nodes)
print(G.edges)
