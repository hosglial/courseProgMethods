import copy
import sys
import networkx as nx
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow
import pandas as pd

# from edges import edges, weighted_nodes, source_node
from openpyxl.utils.exceptions import InvalidFileException

from mainwindow import Ui_MainWindow


class GraphModeller:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.graph = nx.Graph()

    def __del__(self):
        plt.clf()

    def init_graph(self, edges, nodes=None):
        self.graph.add_edges_from(edges)

    def show_graph(self):
        pos = nx.planar_layout(self.graph)

        nx.draw_networkx_edges(self.graph, pos, edge_color='b', arrows=False)

        nx.draw_networkx_nodes(self.graph, pos, node_size=10, margins=0)

        nx.draw_networkx_labels(self.graph, pos, font_size=10)

        plt.show()


class App:
    def __init__(self):
        self.imported_graph = GraphModeller()
        self.imported_edges = []

        self.cleared_graph = GraphModeller()
        self.cleared_edges = []

        self.dropped_graph = GraphModeller()
        self.dropped_edges = []

        self.weight_nodes = []

        self.source_node = None

        self.df_edges = None
        self.df_nodes = None

        self.app = QApplication(sys.argv)
        self.Form = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Form)

        self.ui.init_button.clicked.connect(self.import_data)
        self.ui.imported_graph.clicked.connect(self.draw_imported_graph)
        self.ui.cleared_graph.clicked.connect(self.draw_cleared_graph)
        self.ui.drop_button.clicked.connect(self.draw_dropped_graph)

        self.Form.show()
        sys.exit(self.app.exec_())

    @staticmethod
    def drop_error(message):
        mbox = QMessageBox()
        mbox.setText(message)
        mbox.setWindowTitle('Error')
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()

    def import_data(self):
        # импортировать данные с excel
        dialog = QFileDialog()
        try:
            fname = dialog.getOpenFileName(filter='*.xlsx')
            xl = pd.ExcelFile(fname[0], engine='openpyxl')
        except InvalidFileException:
            self.drop_error('File opening error')
            return

        try:
            self.df_edges = xl.parse('Edges')
            self.df_nodes = xl.parse('Nodes')

            # заполнение рёбер графа
            for first, second in zip(self.df_edges['first_node'], self.df_edges['second_node']):
                self.imported_edges.append((first, second))

            # заполнение нод, имеющих вес
            for node in self.df_nodes['weighted_nodes']:
                self.weight_nodes.append(node)

            print(self.imported_edges)
            print(self.weight_nodes)

            # получение ноды-источника
            self.source_node = self.df_nodes['source_node'][0]
            print(self.source_node)

        except (AttributeError, KeyError):
            self.drop_error('Incorrect file')
            return

        # инициализация импортированного графа
        self.imported_graph.init_graph(self.imported_edges)

        self.cleared_edges = [edge for edge in nx.dfs_edges(self.imported_graph.graph, self.source_node)]
        self.cleared_graph.init_graph(self.cleared_edges)

        self.dropped_graph.graph = copy.deepcopy(self.cleared_graph.graph)

        self.drop_unweighted(self.dropped_graph.graph)

    def drop_unweighted(self, graph):
        all_nodes = set(graph.nodes)
        while len(all_nodes) > 0:
            fnodes = list(
                filter(
                    lambda x: nx.degree(graph, x) == 1 and x not in self.source_node and x not in self.weight_nodes,
                    graph.nodes))
            for node in fnodes:
                graph.remove_node(node)
            if len(fnodes) == 0:
                break
        return graph

    def draw_imported_graph(self):
        self.imported_graph.show_graph()

    def draw_cleared_graph(self):
        self.cleared_graph.show_graph()

    def draw_dropped_graph(self):
        self.dropped_graph.show_graph()



app = App()

app.import_data()
#
# app.draw_imported_graph()
#
# app.draw_cleared_graph()

#
#
#
#
#
# Gr1 = nx.Graph()
#
# draw_all = True
#
# Gr1.add_edges_from(edges)
#
# all_edges = [edge for edge in Gr1.edges()]
#
# green_edges = [edge for edge in nx.dfs_edges(Gr1, 'Кем ТЭЦ')]  # подключенный подграф
# black_edges = [edge for edge in Gr1.edges() if edge not in green_edges]  # неподключенный подграф
#
# edge_colours = ['black' if not edge in green_edges else 'green'
#                 for edge in Gr1.edges()]
#
# nodeset = set()
# for n1, n2 in green_edges:
#     nodeset.add(n1)
#     nodeset.add(n2)
#
# G = nx.Graph()
#
# # рисуем связи
#
# if draw_all:
#     G.add_edges_from(all_edges)
#     pos = nx.planar_layout(G)
#
#     nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='r', arrows=False)
#
#     nx.draw_networkx_nodes(G, pos, node_size=10, margins=0)
#
#     nx.draw_networkx_labels(G, pos, font_size=10)
# else:
#     G.add_edges_from(green_edges)
#     pos = nx.planar_layout(G, center=(10, 10), scale=10)
#
#     nx.draw_networkx_nodes(G, pos, nodelist=list(nodeset), node_size=10, margins=0)  # рисуем все ноды
#
#     nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='g', arrows=False)
#
#     nx.draw_networkx_labels(G, pos, labels={k: k for k in nodeset}, font_size=10)  # рисуем все подписи
#
#
#
# # print(list(nx.neighbors(Gr2,'ТК-41/1')))
# # for i in nx.neighbors(Gr2,'ТК-41/1'):
# #     print(i)
#
#
#
#
#
#
#
#
#
#
# drop_unweighted(Graph=G)
#
# plt.clf()
#
# pos = nx.planar_layout(G, center=(10, 10), scale=10)
#
# nx.draw_networkx_nodes(G, pos, node_size=10, margins=0)  # рисуем все ноды
#
# nx.draw_networkx_edges(G, pos, edge_color='g', arrows=False)
#
# nx.draw_networkx_labels(G, pos, font_size=10)  # рисуем все подписи
#
# plt.show()
