import networkx as nx
import matplotlib.pyplot as plt
from edges import edges, weighted_nodes, source_node

Gr1 = nx.Graph()

draw_all = True

Gr1.add_edges_from(edges)

all_edges = [edge for edge in Gr1.edges()]

green_edges = [edge for edge in nx.dfs_edges(Gr1, 'Кем ТЭЦ')]  # подключенный подграф
black_edges = [edge for edge in Gr1.edges() if edge not in green_edges]  # неподключенный подграф

edge_colours = ['black' if not edge in green_edges else 'green'
                for edge in Gr1.edges()]

nodeset = set()
for n1, n2 in green_edges:
    nodeset.add(n1)
    nodeset.add(n2)

G = nx.Graph()

# рисуем связи

if draw_all:
    G.add_edges_from(all_edges)
    pos = nx.planar_layout(G)

    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='r', arrows=False)

    nx.draw_networkx_nodes(G, pos, node_size=10, margins=0)

    nx.draw_networkx_labels(G, pos, font_size=10)
else:
    G.add_edges_from(green_edges)
    pos = nx.planar_layout(G, center=(10, 10), scale=10)

    nx.draw_networkx_nodes(G, pos, nodelist=list(nodeset), node_size=10, margins=0)  # рисуем все ноды

    nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='g', arrows=False)

    nx.draw_networkx_labels(G, pos, labels={k: k for k in nodeset}, font_size=10)  # рисуем все подписи

plt.show()

# print(list(nx.neighbors(Gr2,'ТК-41/1')))
# for i in nx.neighbors(Gr2,'ТК-41/1'):
#     print(i)
def drop_unweighted(Graph):
    all_nodes = set(Graph.nodes)
    while len(all_nodes) > 0:
        fnodes = list(filter(lambda x: nx.degree(Graph, x) == 1 and x not in source_node and x not in weighted_nodes, Graph.nodes))
        for node in fnodes:
            Graph.remove_node(node)
        if len(fnodes) == 0:
            break
    return Graph

drop_unweighted(Graph=G)

plt.clf()

pos = nx.planar_layout(G, center=(10, 10), scale=10)

nx.draw_networkx_nodes(G, pos, node_size=10, margins=0)  # рисуем все ноды

nx.draw_networkx_edges(G, pos, edge_color='g', arrows=False)

nx.draw_networkx_labels(G, pos, font_size=10)  # рисуем все подписи

plt.show()