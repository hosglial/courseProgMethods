import sys

import networkx as nx
from PySide2.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow
import pandas as pd

from openpyxl.utils.exceptions import InvalidFileException
from treelib import Tree

from mainwindow import Ui_MainWindow


class GraphModeller:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.graph = nx.Graph()

    def init_graph(self, edges):
        self.graph.add_edges_from(edges)


class App:
    def __init__(self):
        self.imported_graph = GraphModeller()
        self.imported_edges = []

        self.numbered_edges = {}
        self.numbered_nodes = {}

        self.source_nodes = {}

        self.treeMass = []

        self.df_edges = None
        self.df_nodes = None

        self.app = QApplication(sys.argv)
        self.Form = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Form)

        self.ui.init_button.clicked.connect(self.import_data)
        self.ui.export_button.clicked.connect(self.export_linked_graph)
        self.ui.show_button.clicked.connect(self.draw_linked_graph)

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
            self.drop_error('Ошибка открытия файла')
            return

        try:
            self.df_edges = xl.parse('Ребра графа')
            self.df_nodes = xl.parse('Источники')

            xl.close()
            for first, second in zip(self.df_edges['Начало'], self.df_edges['Конец']):
                self.imported_edges.append((first, second))

            for node, num in zip(self.df_nodes['Наименование'], self.df_nodes['Номер источника']):
                self.source_nodes[node] = num

        except (AttributeError, KeyError, ValueError):
            self.drop_error('Некорректный файл')
            return

        self.init_graphs()

    def init_graphs(self):
        self.imported_graph.init_graph(self.imported_edges)

        self.numbered_edges.clear()
        self.numbered_nodes.clear()

        self.treeMass = []

        for number, source_node in enumerate(self.source_nodes):
            source_subgraph = list(nx.dfs_edges(self.imported_graph.graph, source_node))
            source_subnodes = list(nx.dfs_tree(self.imported_graph.graph, source_node))

            for edge in source_subgraph:
                self.numbered_edges[edge] = self.source_nodes[source_node]

            for node in source_subnodes:
                self.numbered_nodes[node] = self.source_nodes[source_node]

            self.treeMass.append(Tree())
            tr = self.treeMass[number]
            for e1, e2 in source_subgraph:
                if e1 not in tr.nodes:
                    tr.create_node(e1, e1)
                tr.create_node(e2, e2, parent=e1)

        self.ui.show_button.setEnabled(True)
        self.ui.export_button.setEnabled(True)

    def draw_linked_graph(self):
        for i in self.treeMass:
            i.show()
            i.save2file('tree')

    def export_linked_graph(self):
        self.subgraph_df = pd.DataFrame(columns=['Начало', 'Конец', 'Номер подкл. источника'])
        self.subgraph_df_nodes = pd.DataFrame(columns=['Наименование', 'Номер подкл. источника'])

        for edge in self.imported_edges:
            self.subgraph_df = self.subgraph_df.append(
                {
                    'Начало': edge[0],
                    'Конец': edge[1],
                    'Номер подкл. источника': self.numbered_edges.get(edge, 0)
                }, ignore_index=True)

        for node in self.imported_graph.graph.nodes:
            self.subgraph_df_nodes = self.subgraph_df_nodes.append(
                {
                    'Наименование': node,
                    'Номер подкл. источника': self.numbered_nodes.get(node, 0)
                }, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('Ошибка сохранения')
            return

        try:
            with pd.ExcelWriter(fname[0]) as writer:
                self.subgraph_df.to_excel(writer, sheet_name='count_mark_links')
                self.subgraph_df_nodes.to_excel(writer, sheet_name='count_mark_nodes')
        except PermissionError:
            self.drop_error(
                'Ошибка экспорта')

        for i in self.treeMass:
            i.save2file(list(i.nodes.keys())[0])


app = App()

app.import_data()
