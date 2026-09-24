"""
mati_utils.py — funciones de dibujo compartidas para los notebooks de MATI.

Por qué existe este archivo: dibujar un grafo con Matplotlib requiere varias
líneas de código (calcular una posición para cada nodo, elegir colores,
poner etiquetas...). En vez de repetir ese código en cada notebook, lo
dejamos aquí UNA vez, bien comentado, y en cada notebook simplemente
hacemos:

    from mati_utils import dibujar_grafo, dibujar_multigrafo, SEED

Import: como este archivo vive en la misma carpeta `notebooks/` que los
.ipynb, Python lo encuentra sin configuración adicional.
"""

import networkx as nx
import matplotlib.pyplot as plt

# Semilla fija para el cálculo de posiciones (nx.spring_layout, etc.).
# Con la misma semilla, el dibujo de un grafo sale siempre igual al volver
# a ejecutar la celda — importante para que las figuras sean reproducibles.
SEED = 42


def dibujar_grafo(G, titulo="", pos=None, ax=None, color_nodos="skyblue",
                   guardar_como=None):
    """Dibuja un grafo simple, dirigido o ponderado G con Matplotlib.

    Parámetros:
        G: el grafo a dibujar (nx.Graph, nx.DiGraph, ...).
        titulo: texto que aparece encima del dibujo.
        pos: posiciones de los nodos ya calculadas (dict nodo -> (x, y)).
             Si no se indica, se calculan automáticamente con spring_layout.
        ax: eje de Matplotlib donde dibujar. Si no se indica, se crea una
            figura nueva y se muestra directamente (plt.show()).
        color_nodos: color de relleno de los nodos.
        guardar_como: ruta de archivo (p. ej. "figura1.png") si además de
            mostrar el dibujo se quiere guardar como imagen suelta, útil
            para incluirla en un documento entregable.

    Devuelve: el diccionario de posiciones `pos` usado, por si se quiere
    reutilizar en otro dibujo (p. ej. para comparar el grafo con y sin un
    subconjunto de aristas resaltado, usando exactamente la misma disposición).
    """
    figura_propia = ax is None
    if figura_propia:
        fig, ax = plt.subplots()
    if pos is None:
        pos = nx.spring_layout(G, seed=SEED)

    nx.draw(G, pos, ax=ax, with_labels=True, node_color=color_nodos,
            edge_color='black', node_size=550, font_weight='bold', font_size=9)

    # Si el grafo tiene pesos en las aristas, los mostramos como etiquetas
    pesos = nx.get_edge_attributes(G, 'weight')
    if pesos:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, ax=ax)

    ax.set_title(titulo)
    ax.axis('off')

    if guardar_como is not None:
        plt.savefig(guardar_como, bbox_inches='tight', dpi=150)

    if figura_propia:
        plt.tight_layout()
        plt.show()

    return pos


def dibujar_multigrafo(M, titulo="", pos=None, ax=None, color_nodos="lightsalmon",
                        guardar_como=None):
    """Dibuja un multigrafo M (nx.MultiGraph / nx.MultiDiGraph).

    Un multigrafo puede tener varias aristas paralelas entre el mismo par de
    nodos; dibujarlas todas superpuestas sería ilegible. En vez de eso,
    dibujamos una sola línea por pareja de nodos con una etiqueta "×n" que
    indica cuántas aristas paralelas hay realmente entre ellos.

    Mismos parámetros que dibujar_grafo(); devuelve también `pos`.
    """
    figura_propia = ax is None
    if figura_propia:
        fig, ax = plt.subplots()
    if pos is None:
        pos = nx.spring_layout(M, seed=SEED)

    # Contamos cuántas aristas paralelas hay entre cada pareja de nodos
    conteo = {}
    for u, v in M.edges():
        par = tuple(sorted((u, v)))
        conteo[par] = conteo.get(par, 0) + 1

    simple = nx.Graph()
    simple.add_nodes_from(M.nodes())
    for (u, v), n in conteo.items():
        simple.add_edge(u, v, label=f"×{n}")

    nx.draw(simple, pos, ax=ax, with_labels=True, node_color=color_nodos,
            edge_color='black', node_size=550, font_weight='bold', font_size=9)
    nx.draw_networkx_edge_labels(simple, pos, ax=ax,
                                  edge_labels=nx.get_edge_attributes(simple, 'label'))
    ax.set_title(titulo)
    ax.axis('off')

    if guardar_como is not None:
        plt.savefig(guardar_como, bbox_inches='tight', dpi=150)

    if figura_propia:
        plt.tight_layout()
        plt.show()

    return pos
