import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Leer el archivo Excel con las dos columnas de nombres
excel_file = 'nombres_personas.xlsx'  # Nombre del archivo Excel
sheet_name = 'Hoja1'  # Nombre de la hoja en el archivo Excel
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Obtener los nombres de las dos columnas
personas_A = df['Personas 1'].tolist()
personas_B = df['Personas 2'].tolist()

# Crear el grafo dirigido
grafo_seguidores = nx.DiGraph()

# Conexiones dentro de la columna A
for persona in personas_A:
    num_conexiones = random.randint(2, 4)  # Ajuste: entre 2 y 4 conexiones por persona
    conexiones = random.sample(personas_A, num_conexiones)
    for conexion in conexiones:
        if persona != conexion:  # Evitar conexiones consigo mismo
            grafo_seguidores.add_edge(persona, conexion)

# Conexiones dentro de la columna B
for persona in personas_B:
    num_conexiones = random.randint(2, 4)  # Ajuste: entre 2 y 4 conexiones por persona
    conexiones = random.sample(personas_B, num_conexiones)
    for conexion in conexiones:
        if persona != conexion:  # Evitar conexiones consigo mismo
            grafo_seguidores.add_edge(persona, conexion)

# Conexiones entre las columnas A y B
for persona_A in personas_A:
    num_conexiones = random.randint(2, 4)  # Ajuste: entre 2 y 4 conexiones por persona
    conexiones = random.sample(personas_B, num_conexiones)
    for conexion in conexiones:
        grafo_seguidores.add_edge(persona_A, conexion)

# Ajustar el diseño del grafo para nodos espaciados
pos = nx.spring_layout(grafo_seguidores, k=0.25, iterations=50, seed=42)  # Ajuste: k más bajo y más iteraciones

# Dibujar el grafo
plt.figure(figsize=(16, 12))  # Ajuste: tamaño más grande
nx.draw(grafo_seguidores, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', font_size=10)

# Dijkstra para encontrar las rutas más cortas desde un nodo fuente
def dijkstra_shortest_paths(graph, source):
    lengths, paths = nx.single_source_dijkstra(graph, source=source, weight='weight')
    return lengths, paths

# Elegir un nodo fuente para aplicar Dijkstra (por ejemplo, una persona aleatoria)
source_node = random.choice(list(grafo_seguidores.nodes))
lengths, paths = dijkstra_shortest_paths(grafo_seguidores, source_node)

# Imprimir las rutas más cortas y las distancias desde el nodo fuente a todos los demás nodos
print(f"Rutas más cortas desde el nodo {source_node}:")
for target_node in lengths:
    print(f"Distancia a {target_node}: {lengths[target_node]}, Ruta: {paths[target_node]}")

# Obtener las aristas de las rutas más cortas encontradas por Dijkstra
shortest_path_edges = []
for target_node in paths:
    path = paths[target_node]
    for i in range(len(path) - 1):
        shortest_path_edges.append((path[i], path[i + 1]))

# Dibujar las aristas de las rutas más cortas con un color diferente
nx.draw_networkx_edges(grafo_seguidores, pos, edgelist=shortest_path_edges, edge_color='red', width=2.0)

plt.title("Grafo de Seguidores con Rutas más Cortas", fontsize=15)
plt.show()
