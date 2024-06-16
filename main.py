import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

class GraphView(QGraphicsView):
    def __init__(self, graph, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = graph
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.update_view()

    def update_view(self):
        self.scene.clear()
        for node in self.graph.nodes:
            self.scene.addEllipse(node[0], node[1], 20, 20, QPen(Qt.black), QBrush(Qt.blue))
        for edge in self.graph.edges:
            self.scene.addLine(edge[0][0], edge[0][1], edge[1][0], edge[1][1], QPen(Qt.black))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph = Graph()
        self.graph_view = GraphView(self.graph)

        self.node_x_input = QLineEdit(self)
        self.node_y_input = QLineEdit(self)
        self.add_node_button = QPushButton("Add Node", self)
        self.add_node_button.clicked.connect(self.add_node)

        self.edge_start_input = QLineEdit(self)
        self.edge_end_input = QLineEdit(self)
        self.add_edge_button = QPushButton("Add Edge", self)
        self.add_edge_button.clicked.connect(self.add_edge)

        layout = QVBoxLayout()
        layout.addWidget(self.graph_view)
        layout.addWidget(QLabel("Node X:"))
        layout.addWidget(self.node_x_input)
        layout.addWidget(QLabel("Node Y:"))
        layout.addWidget(self.node_y_input)
        layout.addWidget(self.add_node_button)
        layout.addWidget(QLabel("Edge Start (node index):"))
        layout.addWidget(self.edge_start_input)
        layout.addWidget(QLabel("Edge End (node index):"))
        layout.addWidget(self.edge_end_input)
        layout.addWidget(self.add_edge_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setWindowTitle("Graph Visualizer")
        self.setGeometry(100, 100, 800, 600)

    def add_node(self):
        try:
            x = int(self.node_x_input.text())
            y = int(self.node_y_input.text())
            self.graph.add_node((x, y))
            self.graph_view.update_view()
        except ValueError:
            pass

    def add_edge(self):
        try:
            start_index = int(self.edge_start_input.text())
            end_index = int(self.edge_end_input.text())
            if start_index < len(self.graph.nodes) and end_index < len(self.graph.nodes):
                start_node = self.graph.nodes[start_index]
                end_node = self.graph.nodes[end_index]
                self.graph.add_edge((start_node, end_node))
                self.graph_view.update_view()
        except ValueError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
