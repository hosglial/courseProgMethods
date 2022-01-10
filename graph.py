import copy
import sys
from pprint import pprint

import networkx as nx
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow
import pandas as pd
from treelib import Tree

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
        self.counted_nodes = {}
        self.imported_graph = GraphModeller()
        self.imported_edges = []

        self.cleared_graph = GraphModeller()
        self.cleared_edges = []

        self.eq_graph = GraphModeller()
        self.dropped_edges = []

        self.weight_nodes = {}

        self.source_node = None

        self.df_edges = None
        self.df_nodes = None

        self.app = QApplication(sys.argv)
        self.Form = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Form)

        self.ui.init_button.clicked.connect(self.import_data)
        self.ui.button_source.clicked.connect(self.draw_imported_graph)
        self.ui.source_box.currentIndexChanged.connect(self.change_source)
        self.ui.excel_button_3.clicked.connect(self.export_eq_graph)
        self.ui.button_cleared.clicked.connect(self.draw_cleared_graph)

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

        self.eq_graph.graph = copy.deepcopy(self.cleared_graph.graph)

        self.equvalent(self.eq_graph.graph)

        self.ui.button_source.setEnabled(True)
        self.ui.excel_button_3.setEnabled(True)
        self.ui.button_cleared.setEnabled(True)

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
            for node, weight in zip(self.df_nodes['weighted_nodes'], self.df_nodes['weight']):
                self.weight_nodes[node] = weight


        except (AttributeError, KeyError, ValueError):
            self.drop_error('Incorrect file')
            return

        self.init_graphs()

    new_dict = {}

    def count_data(self, node) -> None:
        if not isinstance(node, dict):
            node = {node: {}}

        node = node[list(node.keys())[0]]

        if node.get('children'):
            for child in node['children']:
                self.count_data(child)
            try:
                node['data'] += sum(child[list(child.keys())[0]]['data'] for child in node['children'])
            except KeyError:
                print(node)

    def dfs(self, node):
        node_data = node[list(node.keys())[0]]

        if node_data.get('children'):
            for child in node_data['children']:
                self.dfs(child)
        self.counted_nodes[list(node.keys())[0]] = node_data['data']

    def equvalent(self, graph):
        tr = Tree()
        tr.create_node(self.cleared_edges[0][0], self.cleared_edges[0][0], data=0)
        tr.create_node(self.cleared_edges[0][1], self.cleared_edges[0][1], parent=self.cleared_edges[0][0], data=0)
        for e1, e2 in self.cleared_edges[1:]:
            tr.create_node(e2, e2, parent=e1, data=self.weight_nodes[e2] if e2 in self.weight_nodes else 0)

        tr_dict = tr.to_dict(with_data=True)

        self.count_data(tr_dict)

        self.dfs(tr_dict)

        pprint(self.counted_nodes)

        return graph

    def draw_imported_graph(self):
        self.imported_graph.show_graph()

    def draw_cleared_graph(self):
        self.cleared_graph.show_graph()

    def export_eq_graph(self):
        self.cleared_graph.show_graph()


app = App()

app.import_data()
