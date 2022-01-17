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
        for e in edges:
            self.graph.add_edge(e[0], e[1], weight=e[2] if len(e) == 3 else 0)

    def show_graph(self):
        plt.clf()

        pos = nx.planar_layout(self.graph)

        nx.draw_networkx_edges(self.graph, pos, edge_color='b', arrows=False)

        nx.draw_networkx_nodes(self.graph, pos, node_size=10, margins=0)

        nx.draw_networkx_labels(self.graph, pos, font_size=10)

        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)


class App:
    def __init__(self):
        self.weight_cleared_nodes = {}
        self.imported_graph = GraphModeller()
        self.imported_edges = []

        self.cleared_graph = GraphModeller()
        self.cleared_edges = []
        self.counted_edges = []
        self.counted_nodes = {}

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
        self.ui.source_box.setDuplicatesEnabled(False)

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

        self.cleared_graph.graph.clear()
        self.eq_graph.graph.clear()

        for node in self.imported_graph.graph.nodes:
            self.ui.source_box.addItem(node)

        self.ui.source_box.setEnabled(True)

        # получение подграфа подключенного к источнику
        self.cleared_edges = [edge for edge in nx.bfs_edges(self.imported_graph.graph, self.source_node)]
        self.cleared_graph.init_graph(self.cleared_edges)

        self.weight_cleared_nodes.clear()
        for node in self.weight_nodes.keys():
            if node in self.cleared_graph.graph.nodes:
                self.weight_cleared_nodes[node] = self.weight_nodes[node]

        # эквивалентирование
        tr = Tree()
        for e1, e2 in self.cleared_edges:
            if e1 not in tr.nodes:
                tr.create_node(e1, e1, data=self.weight_cleared_nodes[e2] if e2 in self.weight_cleared_nodes else 0)
            tr.create_node(e2, e2, parent=e1,
                           data=self.weight_cleared_nodes[e2] if e2 in self.weight_cleared_nodes else 0)

        tr_dict = tr.to_dict(with_data=True)

        self.count_edges(tr_dict)

        self.take_nodes(tr_dict)

        self.counted_edges.clear()
        for n1, n2 in self.cleared_edges:
            if self.counted_nodes.get(n2, 0) > 0:
                self.counted_edges.append((n1, n2, self.counted_nodes.get(n2, 0)))

        self.eq_graph.init_graph(self.counted_edges)

        self.drop_unweighted(self.eq_graph.graph)

        self.ui.button_source.setEnabled(True)
        self.ui.excel_button_3.setEnabled(True)
        self.ui.button_cleared.setEnabled(True)

    def drop_unweighted(self, graph):
        all_nodes = set(graph.nodes)
        while len(all_nodes) > 0:
            fnodes = list(
                filter(
                    lambda x: nx.degree(graph,
                                        x) == 1 and x not in self.source_node and x not in self.weight_cleared_nodes.keys(),
                    graph.nodes))
            for node in fnodes:
                graph.remove_node(node)
            if len(fnodes) == 0:
                break
        return graph

    def import_data(self):
        # импортировать данные с excel
        dialog = QFileDialog()
        try:
            fname = dialog.getOpenFileName(filter='*.xlsx', directory='/home/ashchigol/PycharmProjects/prog_methods')
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

    def count_edges(self, node) -> None:
        if not isinstance(node, dict):
            node = {node: {}}

        node = node[list(node.keys())[0]]

        if node.get('children'):
            for child in node['children']:
                self.count_edges(child)
            try:
                node['data'] += sum(child[list(child.keys())[0]]['data'] for child in node['children'])
            except KeyError:
                print(node)

    def take_nodes(self, node):
        node_data = node[list(node.keys())[0]]

        if node_data.get('children'):
            for child in node_data['children']:
                self.take_nodes(child)
        self.counted_nodes[list(node.keys())[0]] = node_data['data']

    def draw_imported_graph(self):
        self.imported_graph.show_graph()

    def draw_cleared_graph(self):
        self.eq_graph.show_graph()

    def export_eq_graph(self):
        self.eq_df = pd.DataFrame(columns=['точка1', 'точка2', 'нагрузка','посещена'])
        self.eq_df_nodes = pd.DataFrame(columns=['точка', 'нагрузка', 'посещена'])

        for edge in self.imported_graph.graph.edges:
            if edge not in self.eq_graph.graph.edges:
                self.eq_df = self.eq_df.append(
                    {'точка1': edge[0], 'точка2': edge[1], 'нагрузка': self.weight_nodes.get(edge[1], 0),
                     'посещена': False},
                    ignore_index=True)
            else:
                self.eq_df = self.eq_df.append(
                    {'точка1': edge[0], 'точка2': edge[1], 'нагрузка': self.counted_nodes.get(edge[1], 0),
                     'посещена': True},
                    ignore_index=True)

        for node in self.imported_graph.graph.nodes:
            if node in self.eq_graph.graph.nodes:
                self.eq_df_nodes = self.eq_df_nodes.append(
                    {'точка': node, 'нагрузка': self.counted_nodes[node], 'посещена': True}, ignore_index=True)
            elif node in self.weight_nodes:
                self.eq_df_nodes = self.eq_df_nodes.append(
                    {'точка': node, 'нагрузка': self.weight_nodes[node], 'посещена': False}, ignore_index=True)
            else:
                self.eq_df_nodes = self.eq_df_nodes.append(
                    {'точка': node, 'нагрузка': 0, 'посещена': False}, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('Ошибка сохранения файла')
            return

        try:
            with pd.ExcelWriter(fname[0]) as writer:
                self.eq_df.to_excel(writer, sheet_name='edges')
                self.eq_df_nodes.to_excel(writer, sheet_name='nodes')
        except PermissionError:
            self.drop_error(
                'Ошибка экспорта, сохраняемый файл недоступен для редактирования\nЗакройте сохраняемый файл')


app = App()

app.import_data()
