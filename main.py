import sys
import pandas as pd
import random
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QSplitter, QDialog
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SubgraphWindow(QDialog):
    def __init__(self, subgraph):
        super().__init__()
        self.subgraph = subgraph
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Subgraph Shortest Path')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.draw_subgraph()

    def draw_subgraph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        pos = nx.spring_layout(self.subgraph)
        nx.draw(self.subgraph, pos, with_labels=True, node_size=500, node_color='orange', edge_color='red', width=2, ax=ax)
        self.canvas.draw()

class GraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear el grafo desde el archivo Excel
        self.graph = self.create_graph_from_excel('nombres_personas.xlsx')
        self.names = list(self.graph.nodes)

        # Configurar la interfaz de usuario
        self.initUI()

    def create_graph_from_excel(self, excel_file):
        df = pd.read_excel(excel_file, sheet_name='Hoja1')
        personas_A = df['Personas 1'].astype(str).tolist()  # Convertir a cadenas
        personas_B = df['Personas 2'].astype(str).tolist()  # Convertir a cadenas

        G = nx.DiGraph()

        # Conexiones dentro de la columna A
        for persona in personas_A:
            num_conexiones = random.randint(2, 4)
            conexiones = random.sample(personas_A, num_conexiones)
            for conexion in conexiones:
                if persona != conexion:
                    G.add_edge(persona, conexion)

        # Conexiones dentro de la columna B
        for persona in personas_B:
            num_conexiones = random.randint(2, 4)
            conexiones = random.sample(personas_B, num_conexiones)
            for conexion in conexiones:
                if persona != conexion:
                    G.add_edge(persona, conexion)

        # Conexiones entre las columnas A y B
        for persona_A in personas_A:
            num_conexiones = random.randint(2, 4)
            conexiones = random.sample(personas_B, num_conexiones)
            for conexion in conexiones:
                G.add_edge(persona_A, conexion)

        return G

    def initUI(self):
        self.setWindowTitle('Graph Shortest Path Finder')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout()

        self.combo_box_1 = QComboBox()
        self.combo_box_2 = QComboBox()
        for name in self.names:
            self.combo_box_1.addItem(name)
            self.combo_box_2.addItem(name)

        find_button = QPushButton('Find Shortest Path')
        find_button.clicked.connect(self.find_shortest_path)

        self.result_label = QLabel('Shortest Path: ')
        self.result_label.setWordWrap(True)

        left_layout.addWidget(self.combo_box_1)
        left_layout.addWidget(self.combo_box_2)
        left_layout.addWidget(find_button)
        left_layout.addWidget(self.result_label)

        left_widget.setLayout(left_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        splitter.addWidget(left_widget)
        splitter.addWidget(self.canvas)

        layout.addWidget(splitter)

        central_widget.setLayout(layout)

        self.draw_graph()

    def draw_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='skyblue', ax=ax)
        self.canvas.draw()

    def find_shortest_path(self):
        person1 = self.combo_box_1.currentText()
        person2 = self.combo_box_2.currentText()
        if person1 and person2:
            try:
                shortest_path = nx.dijkstra_path(self.graph, person1, person2)
                self.result_label.setText(f'Shortest Path: {" -> ".join(shortest_path)}')

                subgraph = self.graph.subgraph(shortest_path).copy()
                self.show_subgraph(subgraph)

            except nx.NetworkXNoPath:
                self.result_label.setText('No path exists between the selected persons.')

    def show_subgraph(self, subgraph):
        self.subgraph_window = SubgraphWindow(subgraph)
        self.subgraph_window.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphApp()
    ex.show()
    sys.exit(app.exec_())
