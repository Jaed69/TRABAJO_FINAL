import sys
import pandas as pd
import random
import networkx as nx
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
                             QComboBox, QSplitter, QDialog, QLineEdit, QFormLayout, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import graphviz

class VentanaGraphviz(QDialog):
    def __init__(self, dot_source, titulo='Visualización de Camino Más Corto'):
        super().__init__()
        self.dot_source = dot_source
        self.titulo = titulo
        self.iniciarUI()

    def iniciarUI(self):
        self.setWindowTitle(self.titulo)
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignCenter)  # Centrar la imagen
        layout.addWidget(self.label_imagen)
        self.setLayout(layout)
        self.mostrarGraphviz()

    def mostrarGraphviz(self):
        dot = graphviz.Source(self.dot_source)
        dot.format = 'png'
        dot_path = 'graphviz_output'
        dot.render(dot_path, format='png', cleanup=True)
        self.label_imagen.setPixmap(QPixmap(f"{dot_path}.png"))

class AplicacionGrafo(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear el grafo desde el archivo Excel
        self.grafo = self.crearGrafosDesdeExcel('nombres_personas.xlsx')
        self.nombres = list(self.grafo.nodes)

        # Configurar la interfaz de usuario
        self.iniciarUI()

    def crearGrafosDesdeExcel(self, archivo_excel):
        df = pd.read_excel(archivo_excel, sheet_name='Hoja1')
        personas_A = df['Personas 1'].astype(str).tolist()
        personas_B = df['Personas 2'].astype(str).tolist()

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

    def iniciarUI(self):
        self.setWindowTitle('Trabajo Final Complejidad')
        self.setGeometry(100, 100, 1600, 900)  # Aumentamos el tamaño de la ventana principal

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout = QVBoxLayout()

        divisor = QSplitter(Qt.Horizontal)

        widget_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()

        # Estilo para los subtítulos
        estilo_etiqueta = """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }
        """

        self.etiqueta_origen = QLabel('Origen')
        self.etiqueta_origen.setStyleSheet(estilo_etiqueta)
        self.combo_origen = QComboBox()
        self.etiqueta_destino = QLabel('Destino')
        self.etiqueta_destino.setStyleSheet(estilo_etiqueta)
        self.combo_destino = QComboBox()

        # Estilo para el QComboBox
        estilo_combobox = """
            QComboBox {
                font-size: 18px; /* Tamaño de fuente más grande */
                padding: 10px; /* Aumentar el relleno */
                min-width: 200px; /* Ancho mínimo */
                min-height: 40px; /* Altura mínima */
            }
            QComboBox QAbstractItemView {
                font-size: 18px; /* Tamaño de fuente más grande para las opciones */
                padding: 10px; /* Aumentar el relleno */
            }
        """
        self.combo_origen.setStyleSheet(estilo_combobox)
        self.combo_destino.setStyleSheet(estilo_combobox)

        for nombre in self.nombres:
            self.combo_origen.addItem(nombre)
            self.combo_destino.addItem(nombre)

        boton_encontrar = QPushButton('Encontrar la conexión más corta')
        boton_encontrar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        boton_encontrar.clicked.connect(self.encontrarCaminoMasCorto)

        self.etiqueta_resultado = QLabel('Ruta de Amigos: ')
        self.etiqueta_resultado.setStyleSheet("QLabel { font-size: 14px; }")
        self.etiqueta_resultado.setWordWrap(True)

        # Formulario para agregar nueva persona
        layout_formulario = QFormLayout()
        self.entrada_nueva_persona = QLineEdit()
        self.entrada_nueva_persona.setStyleSheet("""
            QLineEdit {
                font-size: 16px; /* Tamaño de fuente */
                padding: 8px; /* Relleno */
                min-height: 30px; /* Altura mínima */
            }
        """)
        self.spinbox_conexiones = QSpinBox()
        self.spinbox_conexiones.setRange(1, 10)
        self.spinbox_conexiones.setStyleSheet("""
            QSpinBox {
                font-size: 16px; /* Tamaño de fuente */
                padding: 8px; /* Relleno */
                min-height: 30px; /* Altura mínima */
            }
        """)
        layout_formulario.addRow('Nombre de nueva persona:', self.entrada_nueva_persona)
        layout_formulario.addRow('Número de Amigos:', self.spinbox_conexiones)

        boton_agregar_persona = QPushButton('Agregar Persona')
        boton_agregar_persona.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #007B9F;
            }
        """)
        boton_agregar_persona.clicked.connect(self.agregarPersona)

        # Botón para mostrar amigos
        boton_mostrar_amigos = QPushButton('Mostrar Amigos')
        boton_mostrar_amigos.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        boton_mostrar_amigos.clicked.connect(self.mostrarAmigos)

        # Botón para salir de la aplicación
        boton_salir = QPushButton('Salir')
        boton_salir.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        boton_salir.clicked.connect(QApplication.quit)

        layout_izquierdo.addWidget(self.etiqueta_origen)
        layout_izquierdo.addWidget(self.combo_origen)
        layout_izquierdo.addWidget(self.etiqueta_destino)
        layout_izquierdo.addWidget(self.combo_destino)
        layout_izquierdo.addWidget(boton_encontrar)
        layout_izquierdo.addWidget(self.etiqueta_resultado)
        layout_izquierdo.addLayout(layout_formulario)
        layout_izquierdo.addWidget(boton_agregar_persona)
        layout_izquierdo.addWidget(boton_mostrar_amigos)
        layout_izquierdo.addWidget(boton_salir)

        widget_izquierdo.setLayout(layout_izquierdo)

        self.figura = Figure(figsize=(12, 8))
        self.lienzo = FigureCanvas(self.figura)

        divisor.addWidget(widget_izquierdo)
        divisor.addWidget(self.lienzo)

        layout.addWidget(divisor)

        widget_central.setLayout(layout)

        self.dibujarGrafo()

    def dibujarGrafo(self, algoritmo_layout=nx.spring_layout, **kwargs):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        pos = algoritmo_layout(self.grafo, **kwargs)
        nx.draw(self.grafo, pos, with_labels=True, node_size=400, node_color='orange', edge_color='gray', font_size=10, ax=ax)
        self.lienzo.draw()

    def encontrarCaminoMasCorto(self):
        persona1 = self.combo_origen.currentText()
        persona2 = self.combo_destino.currentText()
        if persona1 and persona2:
            try:
                camino_mas_corto = self.dijkstra(self.grafo, persona1, persona2)
                self.etiqueta_resultado.setText(f'Conexión: {" -> ".join(camino_mas_corto)}')

                # Visualizar el camino más corto con Graphviz
                self.visualizarCaminoGraphviz(camino_mas_corto)

            except ValueError as e:
                self.etiqueta_resultado.setText(str(e))

    def visualizarCaminoGraphviz(self, camino):
        dot = graphviz.Digraph(comment='Camino Más Corto')

        for nodo in camino:
            dot.node(nodo)

        for i in range(len(camino) - 1):
            dot.edge(camino[i], camino[i + 1])

        # Mostrar el gráfico de Graphviz en una ventana emergente
        dot_source = dot.source
        self.ventana_graphviz = VentanaGraphviz(dot_source, titulo='Camino Más Corto')
        self.ventana_graphviz.exec_()

    def dijkstra(self, grafo, inicio, fin):
        distancias = {nodo: float('inf') for nodo in grafo}
        distancias[inicio] = 0
        predecesores = {nodo: None for nodo in grafo}
        nodos_visitados = set()
        nodos_no_visitados = set(grafo.nodes)

        while nodos_no_visitados:
            nodo_actual = min(nodos_no_visitados, key=lambda nodo: distancias[nodo])
            if nodo_actual == fin:
                break
            nodos_no_visitados.remove(nodo_actual)
            nodos_visitados.add(nodo_actual)
            for vecino in grafo.neighbors(nodo_actual):
                if vecino in nodos_visitados:
                    continue
                nueva_distancia = distancias[nodo_actual] + grafo[nodo_actual][vecino].get('weight', 1)
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual

        camino_mas_corto = []
        nodo_actual = fin
        while nodo_actual is not None:
            camino_mas_corto.insert(0, nodo_actual)
            nodo_actual = predecesores[nodo_actual]

        if distancias[fin] == float('inf'):
            raise ValueError(f"No existe ruta entre {inicio} y {fin}.")

        return camino_mas_corto

    def agregarPersona(self):
        nueva_persona = self.entrada_nueva_persona.text()
        num_conexiones = self.spinbox_conexiones.value()
        if nueva_persona and nueva_persona not in self.grafo:
            self.grafo.add_node(nueva_persona)
            self.nombres.append(nueva_persona)
            self.combo_origen.addItem(nueva_persona)
            self.combo_destino.addItem(nueva_persona)
            nodos_existentes = list(self.grafo.nodes)
            nodos_existentes.remove(nueva_persona)
            conexiones = random.sample(nodos_existentes, num_conexiones)
            for conexion in conexiones:
                self.grafo.add_edge(nueva_persona, conexion)
            self.dibujarGrafo()

    def mostrarAmigos(self):
        persona_seleccionada = self.combo_origen.currentText()
        if persona_seleccionada:
            amigos = list(self.grafo.neighbors(persona_seleccionada))
            amigos.append(persona_seleccionada)
            subgrafo = self.grafo.subgraph(amigos).copy()
            self.mostrarSubgrafo(subgrafo, titulo=f'Amigos de {persona_seleccionada}')

    def mostrarSubgrafo(self, subgrafo, titulo):
        self.ventana_subgrafo = VentanaSubgrafo(subgrafo, titulo=titulo)
        self.ventana_subgrafo.exec_()

class VentanaSubgrafo(QDialog):
    def __init__(self, subgrafo, titulo='Subgrafo'):
        super().__init__()
        self.subgrafo = subgrafo
        self.titulo = titulo
        self.iniciarUI()

    def iniciarUI(self):
        self.setWindowTitle(self.titulo)
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignCenter)  # Centrar la imagen
        layout.addWidget(self.label_imagen)
        self.setLayout(layout)
        self.mostrarSubgrafo()

    def mostrarSubgrafo(self):
        dot = graphviz.Digraph(comment=self.titulo)
        for nodo in self.subgrafo.nodes():
            dot.node(nodo)
        for edge in self.subgrafo.edges():
            dot.edge(edge[0], edge[1])
        dot_path = 'subgrafo_output'
        dot.render(dot_path, format='png', cleanup=True)
        self.label_imagen.setPixmap(QPixmap(f"{dot_path}.png"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AplicacionGrafo()
    ex.show()
    sys.exit(app.exec_())
