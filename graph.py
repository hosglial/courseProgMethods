import copy
import sys
from pprint import pprint

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
        plt.clf()

        pos = nx.planar_layout(self.graph)

        nx.draw_networkx_edges(self.graph, pos, edge_color='b', arrows=False)

        nx.draw_networkx_nodes(self.graph, pos, node_size=10, margins=0)

        nx.draw_networkx_labels(self.graph, pos, font_size=10)


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
        self.ui.button_source.clicked.connect(self.draw_imported_graph)
        self.ui.button_connect.clicked.connect(self.draw_cleared_graph)
        self.ui.button_weight.clicked.connect(self.draw_dropped_graph)
        self.ui.source_box.currentIndexChanged.connect(self.change_source)
        self.ui.excel_button_2.clicked.connect(self.export_cleared_graph)
        self.ui.excel_button_3.clicked.connect(self.export_dropped_graph)

        plt.ion()
        plt.show()

        self.Form.show()
        sys.exit(self.app.exec_())

    @staticmethod
    def drop_error(message):
        mbox = QMessageBox()
        mbox.setText(message)
        mbox.setWindowTitle('Error')
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()

    def change_source(self):
        self.source_node = self.ui.source_box.currentText()
        print(self.source_node)
        self.init_graphs()

    def init_graphs(self):
        # инициализация импортированного графа
        self.imported_graph.init_graph(self.imported_edges)

        for node in self.imported_graph.graph.nodes:
            self.ui.source_box.addItem(node)

        self.ui.source_box.setEnabled(True)

        self.cleared_edges = [edge for edge in nx.dfs_edges(self.imported_graph.graph, self.source_node)]
        self.cleared_graph.init_graph(self.cleared_edges)

        self.dropped_graph.graph = copy.deepcopy(self.cleared_graph.graph)

        self.drop_unweighted(self.dropped_graph.graph)

        self.ui.button_source.setEnabled(True)
        self.ui.button_weight.setEnabled(True)
        self.ui.button_connect.setEnabled(True)
        self.ui.excel_button_2.setEnabled(True)
        self.ui.excel_button_3.setEnabled(True)

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

            xl.close()
            # заполнение рёбер графа
            for first, second in zip(self.df_edges['first_node'], self.df_edges['second_node']):
                self.imported_edges.append((first, second))

            if len(list(self.df_edges['first_node'])) != len(list(self.df_edges['second_node'])):
                self.drop_error('Incorrect edges data')
                return

            # заполнение нод, имеющих вес
            for node in self.df_nodes['weighted_nodes']:
                self.weight_nodes.append(node)
                if node not in list(self.df_edges['first_node']) and node not in list(self.df_edges['second_node']):
                    self.drop_error(f'Weighted node: {node} not present in edges')
                    return

            # print(self.imported_edges)
            # print(self.weight_nodes)

        except (AttributeError, KeyError, ValueError):
            self.drop_error('Incorrect file')
            return

        self.init_graphs()

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
        unvisited_edges = list(self.imported_graph.graph.nodes)
        graph_num = 1
        while unvisited_edges:
            dfs = list(nx.dfs_edges(self.imported_graph.graph, unvisited_edges[0]))
            current_subdgraph = [edge1 for edge1, edge2 in dfs] + [edge2 for edge1, edge2 in dfs]
            for i in current_subdgraph:
                if i in unvisited_edges:
                    unvisited_edges.remove(i)
            print(graph_num)
            graph_num += 1
            print(current_subdgraph)

        self.cleared_graph.show_graph()

    def draw_dropped_graph(self):
        self.dropped_graph.show_graph()

    def export_cleared_graph(self):
        self.cleared_df = pd.DataFrame(columns=['first_node', 'second_node'])
        for edge in self.cleared_graph.graph.edges:
            self.cleared_df = self.cleared_df.append({'first_node': edge[0], 'second_node': edge[1]}, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('File saving error')
            return

        try:
            self.cleared_df.to_excel(fname[0])
        except PermissionError:
            self.drop_error(
                'Export error,the exported file is not available for editing.\nClose the exported file')

    def export_dropped_graph(self):
        self.dropped_df = pd.DataFrame(columns=['first_node', 'second_node'])
        for edge in self.dropped_graph.graph.edges:
            self.dropped_df = self.dropped_df.append({'first_node': edge[0], 'second_node': edge[1]}, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('File saving error')
            return

        try:
            self.dropped_df.to_excel(fname[0])
        except PermissionError:
            self.drop_error(
                'Export error,the exported file is not available for editing.\nClose the exported file')

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
