import copy
import sys
from pprint import pprint

import networkx as nx
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow
import pandas as pd
from treelib import Tree
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


class App:
    def __init__(self):
        self.imported_graph = GraphModeller()
        self.imported_edges = []

        self.cleared_graph = GraphModeller()
        self.cleared_edges = []
        self.counted_edges = []
        self.counted_nodes = {}

        self.eq_graph = GraphModeller()

        self.weight_nodes = {}

        self.source_node = None

        self.df_edges = None
        self.df_nodes = None

        self.app = QApplication(sys.argv)
        self.Form = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Form)

        self.ui.init_button.clicked.connect(self.import_data)
        self.ui.source_box.currentIndexChanged.connect(self.change_source)
        self.ui.excel_button_3.clicked.connect(self.export_eq_graph)
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

        self.drop_unweighted(self.cleared_graph.graph)

        self.cleared_edges = [edge for edge in nx.dfs_edges(self.imported_graph.graph, self.source_node)]

        # эквивалентирование
        tr = Tree()
        tr.create_node(self.cleared_edges[0][0], self.cleared_edges[0][0], data=0)
        tr.create_node(self.cleared_edges[0][1], self.cleared_edges[0][1], parent=self.cleared_edges[0][0], data=0)
        for e1, e2 in self.cleared_edges[1:]:
            tr.create_node(e2, e2, parent=e1, data=self.weight_nodes[e2] if e2 in self.weight_nodes else 0)

        tr_dict = tr.to_dict(with_data=True)

        self.count_data(tr_dict)

        self.dfs(tr_dict)

        pprint(self.counted_nodes)

        for n1, n2 in self.cleared_edges:
            self.counted_edges.append((n1, n2, self.counted_nodes.get(n2, 0)))

        self.cleared_graph.init_graph(self.counted_edges)

        self.eq_graph.graph = copy.deepcopy(self.cleared_graph.graph)

        self.ui.excel_button_3.setEnabled(True)

    def drop_unweighted(self, graph):
        all_nodes = set(graph.nodes)
        while len(all_nodes) > 0:
            fnodes = list(
                filter(
                    lambda x: nx.degree(graph,
                                        x) == 1 and x not in self.source_node and x not in self.weight_nodes.keys(),
                    graph.nodes))
            for node in fnodes:
                graph.remove_node(node)
            if len(fnodes) == 0:
                break
        return graph

    def import_data(self):
        dialog = QFileDialog()
        try:
            fname = dialog.getOpenFileName(filter='*.xlsx')
            xl = pd.ExcelFile(fname[0], engine='openpyxl')
        except InvalidFileException:
            self.drop_error('Ошибка открытия файла')
            return

        try:
            self.df_edges = xl.parse('Ребра')
            self.df_nodes = xl.parse('Узлы')

            xl.close()
            # заполнение рёбер графа
            for first, second in zip(self.df_edges['Узел 1'], self.df_edges['Узел 2']):
                self.imported_edges.append((first, second))

            # заполнение нод, имеющих вес
            for node, weight in zip(self.df_nodes['Наименование узла'], self.df_nodes['Нагрузка узла']):
                self.weight_nodes[node] = weight

        except (AttributeError, KeyError, ValueError):
            self.drop_error('Некорректный файл')
            return

        self.init_graphs()

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

    def export_eq_graph(self):
        self.eq_df = pd.DataFrame(columns=['Узел 1', 'Узел 2', 'Нагрузка ребра'])
        self.eq_df_nodes = pd.DataFrame(columns=['Наименование узла', 'Нагрузка узла'])

        for edge in self.counted_edges:
            self.eq_df = self.eq_df.append(
                {'Узел 1': edge[0], 'Узел 2': edge[1], 'Нагрузка ребра': edge[2]}, ignore_index=True)

        for node in self.counted_nodes:
            self.eq_df_nodes = self.eq_df_nodes.append(
                {'Наименование узла': node, 'Нагрузка узла': self.counted_nodes[node]}, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('Ошибка сохранения')
            return

        try:
            with pd.ExcelWriter(fname[0]) as writer:
                self.eq_df.to_excel(writer, sheet_name='Ребра')
                self.eq_df_nodes.to_excel(writer, sheet_name='Точки')
        except PermissionError:
            self.drop_error('Ошибка сохранения')


app = App()

app.import_data()
