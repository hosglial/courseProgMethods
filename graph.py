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
        for e in edges:
            self.graph.add_edge(e[0], e[1], weight=e[2] if len(e) == 3 else 0)
        # self.graph.add_edges_from(edges)

    def show_graph(self, numbers, names):
        plt.clf()

        pos = nx.planar_layout(self.graph)

        nx.draw_networkx_edges(self.graph, pos, edge_color='b', arrows=False, )

        nx.draw_networkx_nodes(self.graph, pos, node_size=10, margins=0)

        if names:
            nx.draw_networkx_labels(self.graph, pos, font_size=10)

        if numbers:
            labels = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)


class App:
    def __init__(self):
        self.imported_graph = GraphModeller()
        self.imported_edges = []

        self.cleared_graph = GraphModeller()
        self.cleared_edges = []

        self.sub_graph = GraphModeller()
        self.sub_edges = []

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
        self.ui.button_connect.clicked.connect(self.draw_sub_graph)
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

        for node in sorted(self.imported_graph.graph.nodes):
            self.ui.source_box.addItem(node)

        self.sub_edges = []
        unvisited_nodes = list(self.imported_graph.graph.nodes)
        graph_num = 1
        while unvisited_nodes:
            current_subgraph = list(nx.dfs_edges(self.imported_graph.graph, unvisited_nodes[0]))
            current_subnodes = list(nx.dfs_tree(self.imported_graph.graph, unvisited_nodes[0]).nodes)

            tree = nx.dfs_tree(self.imported_graph.graph, unvisited_nodes[0])
            print(unvisited_nodes[0])
            for i in current_subnodes:
                unvisited_nodes.remove(i)

            print(graph_num)
            print(current_subgraph)
            for i, v in enumerate(current_subgraph):
                current_subgraph[i] = (v[0], v[1], graph_num)

            self.sub_edges += current_subgraph
            graph_num += 1

        print(self.sub_edges)
        self.sub_graph.init_graph(self.sub_edges)

        self.cleared_edges = [edge for edge in nx.dfs_edges(self.imported_graph.graph, self.source_node)]
        self.cleared_graph.init_graph(self.cleared_edges)

        self.dropped_graph.graph = copy.deepcopy(self.cleared_graph.graph)

        self.drop_unweighted(self.dropped_graph.graph)

        self.ui.source_box.setEnabled(True)
        self.ui.button_source.setEnabled(True)
        self.ui.button_weight.setEnabled(True)
        self.ui.button_connect.setEnabled(True)
        self.ui.excel_button_2.setEnabled(True)
        self.ui.excel_button_3.setEnabled(True)
        self.ui.checkBox_names.setEnabled(True)
        self.ui.checkBox_numbers.setEnabled(True)

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

        except (AttributeError, KeyError, ValueError):
            self.drop_error('Некорректный файл')
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
        self.imported_graph.show_graph(False, True)

    def draw_sub_graph(self):
        self.sub_graph.show_graph(self.ui.checkBox_numbers.isChecked(), self.ui.checkBox_names.isChecked())

    def draw_dropped_graph(self):
        self.dropped_graph.show_graph(False, True)

    def export_cleared_graph(self):
        self.subgraph_df = pd.DataFrame(columns=['first_node', 'second_node', 'subgraph_number'])
        self.subgraph_df_nodes = pd.DataFrame(columns=['node', 'subgraph_number'])

        nodes = {}
        for edge in self.sub_edges:
            self.subgraph_df = self.subgraph_df.append(
                {'first_node': edge[0], 'second_node': edge[1], 'subgraph_number': edge[2]}, ignore_index=True)

            nodes[edge[0]] = edge[2]
            nodes[edge[1]] = edge[2]

        for node in nodes:
            self.subgraph_df_nodes = self.subgraph_df_nodes.append(
                {'node': node, 'subgraph_number': nodes[node]}, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('Ошибка сохранения файла')
            return

        try:
            writer = pd.ExcelWriter(fname[0], writer='openpyxl')
            self.subgraph_df.to_excel(writer, sheet_name='edges')
            self.subgraph_df_nodes.to_excel(writer, sheet_name='nodes')
            writer.save()
            writer.close()
        except PermissionError:
            self.drop_error(
                'Ошибка экспорта, сохраняемый файл недоступен для редактирования\nЗакройте сохраняемый файл')

    def export_dropped_graph(self):
        self.dropped_df = pd.DataFrame(columns=['first_node', 'second_node'])
        for edge in self.dropped_graph.graph.edges:
            self.dropped_df = self.dropped_df.append({'first_node': edge[0], 'second_node': edge[1]}, ignore_index=True)

        dialog = QFileDialog()
        try:
            fname = dialog.getSaveFileName(filter='*.xlsx')
        except InvalidFileException:
            self.drop_error('Ошибка сохранения файла')
            return

        try:
            self.dropped_df.to_excel(fname[0])
        except PermissionError:
            self.drop_error(
                'Ошибка экспорта, сохраняемый файл недоступен для редактирования\nЗакройте сохраняемый файл')


app = App()

app.import_data()
