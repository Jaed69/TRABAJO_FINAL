import sys
import random
import networkx as nx
import pygraphviz as pgv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def create_random_graph():
    G = nx.gnp_random_graph(10, 0.3, directed=True)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 10)
    return G

def draw_graph(G, filename):
    A = nx.nx_agraph.to_agraph(G)
    A.layout(prog='dot')
    A.draw(filename)

def apply_dijkstra(G, source):
    return nx.single_source_dijkstra_path(G, source)

class DijkstraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.graph_label = QLabel("Grafo Original", self)
        self.layout.addWidget(self.graph_label)
        
        self.graph_view = QGraphicsView(self)
        self.layout.addWidget(self.graph_view)
        
        self.result_label = QLabel("Grafo con Dijkstra aplicado", self)
        self.layout.addWidget(self.result_label)
        
        self.result_view = QGraphicsView(self)
        self.layout.addWidget(self.result_view)
        
        self.btn = QPushButton('Generar Grafo y Aplicar Dijkstra', self)
        self.btn.clicked.connect(self.generate_graph)
        self.layout.addWidget(self.btn)
        
        self.setLayout(self.layout)
        self.setWindowTitle('Visualización de Dijkstra')
        self.show()
    
    def generate_graph(self):
        G = create_random_graph()
        
        # Guardar y mostrar el grafo original
        draw_graph(G, 'graph_before.png')
        pixmap = QPixmap('graph_before.png')
        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.graph_view.setScene(scene)
        
        # Aplicar Dijkstra
        source = list(G.nodes())[0]
        dijkstra_path = apply_dijkstra(G, source)
        
        # Dibujar y mostrar el grafo con Dijkstra aplicado
        H = G.copy()
        edges_in_path = [(dijkstra_path[node], node) for node in dijkstra_path if node != source]
        nx.set_edge_attributes(H, {edge: {'color': 'red'} for edge in edges_in_path})
        draw_graph(H, 'graph_after.png')
        pixmap = QPixmap('graph_after.png')
        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.result_view.setScene(scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DijkstraApp()
    sys.exit(app.exec_())
