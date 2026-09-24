# GUÍA DE USO — MATI

Manual de referencia rápido para el cuatrimestre 2026/2027. Complementa a `CLAUDE.md` (que define las convenciones que Claude debe seguir); este documento está pensado para consulta manual del estudiante.

### Cómo trabajar con Claude en este proyecto

Este material parte de la base de que **no tienes experiencia previa en teoría de grafos ni en matemática discreta**, así que no hace falta llegar "sabiendo" nada de antemano. En la práctica esto significa:

- Claude explicará cada concepto nuevo en lenguaje llano antes de usar notación formal, y definirá los términos técnicos la primera vez que aparezcan.
- Cada solución trae siempre una demostración matemática formal, pero acompañada de una explicación paso a paso pensada para alguien que está aprendiendo el tema.
- Se incluyen visualizaciones siempre que ayuden a entender el resultado (no solo como decoración).
- **Puedes preguntar en cualquier momento**, incluso si te parece "básico" — pregunta por un término, por qué se usa un algoritmo y no otro, o pide que se repita el ejemplo con un grafo más pequeño. Es la forma esperada de usar este entorno, no una interrupción.
- **Los notebooks se mantienen deliberadamente cortos y visuales.** Las explicaciones son precisas pero breves (sin párrafos largos), el código lleva comentarios que dicen qué hace cada bloque, y se prioriza un dibujo del grafo frente a un texto que lo describa. Si algún notebook te resulta denso o difícil de seguir, pide que se simplifique — es señal de que hay que recortar, no de que falte estudiar más.

**¿Por qué solo Python (y no SageMath/Gephi)?** El programa de la asignatura los menciona como opción, pero aquí nos quedamos con NetworkX + SymPy + Matplotlib + PyVis, todo dentro de `jupyter lab`. Motivo: es lo único que ya conoces bien, y SageMath (otro kernel) o Gephi (programa externo) añadirían instalación y cambios de contexto sin necesidad real — SymPy ya da precisión simbólica y PyVis ya da interactividad. Si en algún momento un ejercicio concreto lo pide, se puede reconsiderar, pero no es el punto de partida.

---

## 1. Flujo de trabajo diario

### 1.1 Activar el entorno virtual

**PowerShell (Windows):**
```powershell
cd C:\Users\ADMiN\US\MATI
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts, ejecutar una vez (como usuario, no como administrador):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Cuando el entorno está activo, el prompt muestra `(.venv)` al inicio de la línea.

### 1.2 Registrar el kernel del `.venv` (solo la primera vez)

Jupyter Lab necesita saber que existe un intérprete de Python dentro de `.venv` — si no, usará el Python global del sistema y los notebooks fallarán con `ModuleNotFoundError: No module named 'networkx'` (aunque `.venv` tenga todo instalado). Se soluciona una sola vez, con el entorno activado:

```powershell
python -m ipykernel install --user --name mati-venv --display-name "Python (MATI .venv)"
```

Los notebooks de este repositorio ya están configurados para usar este kernel (`mati-venv`) por defecto. Si algún notebook nuevo abre con el kernel equivocado, usa **Kernel → Change Kernel → Python (MATI .venv)**. Este paso solo hay que repetirlo si se borra y recrea `.venv` desde cero.

### 1.3 Levantar Jupyter Lab

Con el entorno activado, este es el único comando que necesitas para trabajar:
```powershell
jupyter lab
```
Esto abre el navegador en `http://localhost:8888/lab` con la raíz del proyecto como directorio de trabajo. Es el flujo habitual: no hace falta ningún otro programa ni editor.

<details>
<summary>Alternativa: conectar desde VS Code (opcional, no necesario)</summary>

1. Abrir la carpeta `C:\Users\ADMiN\US\MATI` en VS Code.
2. Instalar/activar la extensión **Jupyter** (Microsoft).
3. Abrir el `.ipynb` deseado.
4. **Select Kernel → Python Environments** → elegir el intérprete de `.venv` (`.venv\Scripts\python.exe`).

</details>

### 1.4 Crear un notebook nuevo (una entrega = un notebook)

- Ubicación: siempre dentro de `notebooks/`.
- Nomenclatura: `NN_<nombre-de-la-entrega>.ipynb` — dos dígitos (número de entrega/boletín en la plataforma de la universidad) + guion bajo + nombre corto de esa entrega, por ejemplo:
  - `01_cuestionario.ipynb` (ya existente)
  - `02_boletin-grados.ipynb`
- Cada entrega evaluable va en su propio notebook — no se acumulan varias entregas en uno solo.
- Para arrancar uno nuevo rápido, copia `notebooks/_plantilla_ejercicio.ipynb`: trae ya montados los 7 bloques de un ejercicio de ejemplo, listos para sustituir por el enunciado real.

### 1.5 Estructura de cada ejercicio dentro del notebook

Cada ejercicio va separado del siguiente por una línea horizontal (`---`), y usa siempre estos bloques en este orden — cada uno en una caja de color reconocible de un vistazo:

| Bloque | Color | Qué lleva |
|---|---|---|
| 📋 **Enunciado** | gris | El texto original del boletín, tal cual, sin resumir |
| 📚 **Teoría** | azul | Los conceptos mínimos que hacen falta, explicados en lenguaje llano antes que con notación formal |
| 🔢 **Datos** | morado | Qué datos concretos se sacan del enunciado (lista o tabla) + una celda de código que los deja como variables |
| 🧮 **Resolución** | verde | El razonamiento matemático (con LaTeX) que resuelve el ejercicio, breve y riguroso |
| 💻 **Código** | — | La verificación computacional de la Resolución, comentada, con salida visual |
| 🚀 **Ampliación** *(opcional)* | amarillo | Solo si pides una extensión del ejercicio con ayuda de IA |
| 🤖 **Registro de uso de IA** | gris oscuro | Plantilla de la §4 de este documento |

Los bloques **Resolución** y **Código** llevan siempre, en la primera línea, una insignia que dice quién lo hizo:

- `✍️ Trabajo del estudiante` — lo resolviste tú sin ayuda de IA.
- `🤝 Con pistas de IA` — pediste pistas, no la solución.
- `✅ Validado por IA` — resolviste tú y la IA solo revisó/corrigió (lleva una Discusión de 2-4 líneas sobre si tu respuesta era correcta).
- `🤖 Resuelto por IA` — la IA dio la solución completa a petición tuya (también lleva Discusión).

Esto no es burocracia decorativa: es justo lo que pide el departamento para las entregas evaluables (ver más abajo) y además te sirve a ti para ver de un vistazo, al repasar antes de un examen, qué resolviste realmente tú solo.

**Antes de entregar:** `Kernel → Restart Kernel and Run All Cells`, para garantizar que el notebook es reproducible de arriba a abajo sin estado oculto.

### 1.6 Cómo pedir ayuda a la IA (y qué esperar en cada caso)

El flujo normal es: das el enunciado → Claude rellena Enunciado + Teoría + Datos → se detiene, para que lo intentes tú primero. Cuando quieras continuar, dile explícitamente qué necesitas — la respuesta cambia según lo que pidas:

| Si dices algo como... | Obtienes |
|---|---|
| "¿Está bien mi resolución?" / "revisa lo que he hecho" | Una corrección de tu intento, marcada `✅ Validado por IA`, sin rehacer lo que ya estaba bien |
| "dame una pista" / "no sé por dónde seguir, pero no me lo resuelvas" | Una orientación parcial, marcada `🤝 Con pistas de IA` — no obtienes la solución completa aunque insistas un poco |
| "resuélvelo" / "no lo he conseguido, hazlo tú" | La resolución completa, marcada `🤖 Resuelto por IA` |

No hace falta que uses estas frases literalmente, pero cuanto más claro dejes cuál de los tres casos quieres, más preciso será el resultado.

### 1.7 Cómo exportar tu notebook para entregar

La plataforma de la universidad suele pedir el resultado como `.pdf` o similar, no el `.ipynb` en crudo. Para eso está el exportador del proyecto, que ejecuta el notebook y genera el PDF con los resultados ya visibles:

```powershell
.\exportar.ps1 notebooks\00_practica-0.ipynb
```

El PDF aparece en `entregas\`. Las opciones (`--sin-ejecutar`, `--mantener-html`…) y los requisitos están documentados en el **`README.md`**.

Si en algún momento necesitas otro formato, `nbconvert` sigue estando disponible con el entorno activado:

```powershell
# A Markdown (texto + código + figuras como imágenes en una carpeta aparte)
jupyter nbconvert --to markdown notebooks/01_cuestionario.ipynb
```

Si necesitas una figura suelta en `.png`/`.jpg` (por ejemplo para pegarla en un documento aparte), usa el parámetro `guardar_como` de `dibujar_grafo`/`dibujar_multigrafo` (ver §3) al generar esa figura.

> Nota: las celdas con grafos interactivos de PyVis no se ven bien en el PDF/HTML estático (son widgets pensados para explorar en el propio Jupyter Lab); para el entregable apóyate en las figuras de Matplotlib.

---

## 2. Cheat Sheet de NetworkX para MATI

> Cada bloque incluye una línea de contexto en lenguaje llano antes del código, para poder usarlo como referencia aunque no recuerdes la definición formal de memoria.

```python
import networkx as nx
import sympy as sp
import numpy as np
```

### 2.1 Creación de grafos

> Un **grafo** es, intuitivamente, un conjunto de "puntos" (nodos/vértices) unidos por "líneas" (aristas). Es *simple* si entre dos nodos hay como mucho una arista y no hay aristas de un nodo a sí mismo; es *dirigido* si las aristas tienen sentido (como calles de un solo sentido); es *multigrafo* si se permite más de una arista entre el mismo par de nodos; es *bipartito* si los nodos se pueden repartir en dos grupos de forma que todas las aristas van de un grupo al otro (nunca dentro del mismo grupo).

```python
# Grafo simple no dirigido
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

# Grafo dirigido
D = nx.DiGraph()
D.add_edges_from([(1, 2), (2, 3), (3, 1)])

# Multigrafo (aristas paralelas permitidas)
M = nx.MultiGraph()
M.add_edges_from([(1, 2), (1, 2), (2, 3)])

# Multigrafo dirigido
MD = nx.MultiDiGraph()

# Grafo con pesos en aristas
G = nx.Graph()
G.add_weighted_edges_from([(1, 2, 4.5), (2, 3, 2.0), (3, 1, 1.5)])

# Grafo bipartito
from networkx.algorithms import bipartite
B = nx.Graph()
B.add_nodes_from([1, 2, 3], bipartite=0)
B.add_nodes_from(['a', 'b'], bipartite=1)
B.add_edges_from([(1, 'a'), (2, 'a'), (2, 'b'), (3, 'b')])
top, bottom = bipartite.sets(B)          # requiere que B sea conexo
nx.is_bipartite(G)                       # comprobación general (no requiere conexo)

# Desde matriz de adyacencia
A = np.array([[0,1,0],[1,0,1],[0,1,0]])
G = nx.from_numpy_array(A)

# Desde lista de aristas / diccionario
G = nx.from_edgelist([(1,2), (2,3)])
```

### 2.2 Familias notables

> Son grafos "con nombre propio" que aparecen constantemente como ejemplos o contraejemplos: el completo $K_n$ (todos los nodos unidos entre sí), el ciclo $C_n$ (los nodos forman un anillo), el camino $P_n$ (los nodos en fila, sin cerrar el anillo), el bipartito completo $K_{m,n}$ (dos grupos, todas las conexiones posibles entre grupos), la rueda $W_n$ (un ciclo más un nodo central conectado a todos) y el hipercubo $Q_k$ (nodos = vértices de un cubo de dimensión $k$).

```python
n = 5

Kn  = nx.complete_graph(n)                 # Grafo completo K_n
Cn  = nx.cycle_graph(n)                    # Ciclo C_n
Pn  = nx.path_graph(n)                     # Camino P_n
Kmn = nx.complete_bipartite_graph(3, 4)    # Bipartito completo K_{m,n}
Rn  = nx.wheel_graph(n)                    # Rueda W_n (nodo 0 = centro, nx la llama "wheel_graph")
Qk  = nx.hypercube_graph(3)                # Hipercubo Q_k (etiquetas = tuplas binarias)

# Otros útiles
Star = nx.star_graph(n)                    # Grafo estrella
Petersen = nx.petersen_graph()             # Grafo de Petersen (contraejemplo clásico)
Empty = nx.empty_graph(n)                  # Grafo vacío (n nodos, 0 aristas)
```

> `nx.hypercube_graph(k)` etiqueta los nodos como tuplas de 0/1 de longitud `k`; usar `nx.convert_node_labels_to_integers(Qk)` si se necesitan enteros.

### 2.3 Invariantes y conectividad

> El **grado** de un nodo es el número de aristas que tocan a ese nodo (cuántos "vecinos" tiene). Un grafo es **conexo** si se puede llegar de cualquier nodo a cualquier otro caminando por las aristas. Un **punto de articulación** es un nodo que, si se elimina, desconecta el grafo (rompe algún camino); un **puente** es lo mismo pero para una arista. La **conectividad** mide cuántos nodos/aristas como mínimo hay que quitar para desconectar el grafo — cuanto mayor, más "robusto" es.

```python
# Grados
dict(G.degree())                           # {nodo: grado}
sorted((d for _, d in G.degree()), reverse=True)   # secuencia de grados

# Havel-Hakimi: ¿la secuencia es gráfica?
seq = [3, 3, 2, 2, 2]
nx.is_graphical(seq)                       # True/False (test de Erdős–Gallai internamente)

# Componentes conexas (grafo no dirigido)
nx.is_connected(G)
list(nx.connected_components(G))
nx.number_connected_components(G)

# Componentes en dirigidos
nx.is_strongly_connected(D)
nx.is_weakly_connected(D)
list(nx.strongly_connected_components(D))
list(nx.weakly_connected_components(D))

# Puntos de articulación y puentes
list(nx.articulation_points(G))
list(nx.bridges(G))

# Conectividad por nodos / aristas
nx.node_connectivity(G)
nx.edge_connectivity(G)
nx.node_connectivity(G, s=1, t=4)          # entre dos nodos concretos
nx.minimum_node_cut(G)
nx.minimum_edge_cut(G)

# Distancias y excentricidad
nx.shortest_path_length(G, source=1, target=4)
nx.diameter(G)          # requiere G conexo
nx.radius(G)
nx.eccentricity(G)
```

### 2.4 Matrices asociadas (con SymPy para precisión exacta)

> Un grafo se puede representar como una matriz de números para poder calcular cosas con álgebra. La **matriz de adyacencia** dice qué nodos están conectados entre sí (1 si hay arista, 0 si no). La **matriz de incidencia** relaciona nodos con aristas (qué nodos toca cada arista). La **matriz laplaciana** ($L = D - A$, donde $D$ es la matriz de grados) combina ambas ideas y es la base de resultados como el teorema de Matrix-Tree (contar árboles recubridores mediante un determinante).

```python
import sympy as sp

# Matriz de adyacencia -> SymPy exacto
A = sp.Matrix(nx.to_numpy_array(G, dtype=int))

# Matriz de incidencia (nodos x aristas), signo +/-1 según orientación en dirigidos
Inc = sp.Matrix(nx.incidence_matrix(G, oriented=True).toarray())

# Matriz laplaciana L = D - A
L = sp.Matrix(nx.laplacian_matrix(G).toarray())

# Autovalores exactos de la laplaciana (útil para nº de árboles recubridores, Kirchhoff)
L.eigenvals()

# Teorema de Matrix-Tree (Kirchhoff): nº de árboles recubridores
# = cualquier cofactor de L, o el producto de autovalores no nulos / n
import math
cofactor = L.minor_submatrix(0, 0).det()

# Verificación cruzada directa con NetworkX
len(list(nx.spanning_trees(G)))  # solo viable para grafos pequeños (enumeración explícita)

# Rango, determinante, forma escalonada
A.rank()
A.det()
A.rref()
```

### 2.5 Grafos eulerianos y hamiltonianos

> Un **circuito euleriano** es un recorrido que pasa por *todas las aristas* del grafo exactamente una vez y vuelve al punto de partida (el problema original de los puentes de Königsberg). Un **ciclo hamiltoniano** es distinto: pasa por *todos los nodos* exactamente una vez y vuelve al inicio. Que existan circuitos eulerianos se puede comprobar fácilmente con los grados; que exista un ciclo hamiltoniano es, en general, mucho más difícil de determinar (problema NP-completo).

```python
# Eulerianos
nx.is_eulerian(G)                          # circuito euleriano cerrado
nx.has_eulerian_path(G)                    # camino euleriano (abierto o cerrado)
list(nx.eulerian_circuit(G, source=1))     # requiere is_eulerian(G) == True
list(nx.eulerian_path(G))                  # requiere has_eulerian_path(G) == True

# Comprobación manual (criterio de Euler): todos los grados pares (circuito)
# o exactamente 0 o 2 nodos de grado impar (camino), y G conexo (salvo nodos aislados)
grados_impares = [v for v, d in G.degree() if d % 2 != 0]

# Hamiltonianos: NetworkX no trae un test directo de existencia (problema NP-completo)
# Aproximaciones útiles:
from networkx.algorithms.approximation import traveling_salesman_problem
ciclo_aprox = traveling_salesman_problem(G, cycle=True)   # heurística, no exacto

# Búsqueda exacta por fuerza bruta (solo grafos pequeños, uso docente):
import itertools
def tiene_ciclo_hamiltoniano(G):
    nodos = list(G.nodes())
    for perm in itertools.permutations(nodos[1:]):
        ciclo = [nodos[0]] + list(perm) + [nodos[0]]
        if all(G.has_edge(ciclo[i], ciclo[i+1]) for i in range(len(ciclo)-1)):
            return ciclo
    return None
```

### 2.6 Árboles y Árboles Recubridores Mínimos

> Un **árbol** es un grafo conexo sin ciclos (no hay forma de "dar la vuelta" y volver al punto de partida sin repetir arista). Un **árbol recubridor** de un grafo $G$ es un árbol que usa todos los nodos de $G$ pero solo algunas de sus aristas, las justas para mantenerlo conexo sin ciclos. El **árbol recubridor mínimo (MST)** es el que minimiza la suma de los pesos de esas aristas; Kruskal y Prim son dos algoritmos distintos (pero igualmente correctos) para encontrarlo.

```python
# Comprobación de árbol
nx.is_tree(G)
nx.is_forest(G)

# Árbol recubridor mínimo (MST)
T_kruskal = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
T_prim    = nx.minimum_spanning_tree(G, weight='weight', algorithm='prim')

# Aristas del MST y peso total
list(T_kruskal.edges(data='weight'))
T_kruskal.size(weight='weight')

# Traza paso a paso (para justificar el algoritmo en la demostración)
list(nx.minimum_spanning_edges(G, algorithm='kruskal', weight='weight', data=True))

# Árbol recubridor máximo (cambiando el sentido)
T_max = nx.maximum_spanning_tree(G, weight='weight')
```

### 2.7 Complementarios e isomorfismo

> El **grafo complementario** de $G$ tiene los mismos nodos, pero con las aristas "invertidas": hay arista entre dos nodos en $\bar{G}$ exactamente cuando *no* la había en $G$. Dos grafos son **isomorfos** cuando, aunque se dibujen o se nombren los nodos de forma distinta, tienen exactamente la misma estructura de conexiones (existe una forma de renombrar los nodos de uno para que coincida exactamente con el otro).

```python
# Grafo complementario
Gc = nx.complement(G)

# Isomorfismo
nx.is_isomorphic(G1, G2)

# Isomorfismo con verificación de la correspondencia de nodos
from networkx.algorithms.isomorphism import GraphMatcher
gm = GraphMatcher(G1, G2)
gm.is_isomorphic()
gm.mapping                                 # diccionario de correspondencia hallado

# Invariantes rápidos para descartar isomorfismo antes de probar formalmente
sorted(d for _, d in G1.degree()) == sorted(d for _, d in G2.degree())
G1.number_of_nodes() == G2.number_of_nodes()
G1.number_of_edges() == G2.number_of_edges()
```

---

## 3. Visualización

Toda la lógica de dibujo vive ya en `notebooks/mati_utils.py` — no hace falta redefinirla en cada notebook:

```python
from mati_utils import dibujar_grafo, dibujar_multigrafo, SEED

dibujar_grafo(G, titulo="Ejercicio 3 — Árbol recubridor mínimo")

# Para guardar además una imagen suelta (útil al exportar el entregable, §1.6):
dibujar_grafo(G, titulo="Ejercicio 3", guardar_como="ejercicio3.png")
```

Abre `notebooks/mati_utils.py` si quieres ver cómo están hechas — están comentadas paso a paso pensando en alguien sin soltura en Matplotlib.

### Variantes útiles (para casos que `dibujar_grafo` no cubre directamente)

```python
# Resaltar un subconjunto de nodos (p. ej. puntos de articulación)
colores = ["#C44E52" if v in articulaciones else "#4C72B0" for v in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=colores, ...)

# Resaltar un subconjunto de aristas (p. ej. el MST sobre el grafo original)
colores_aristas = ["#C44E52" if e in T.edges() or (e[1], e[0]) in T.edges()
                    else "black" for e in G.edges()]
nx.draw_networkx_edges(G, pos, edge_color=colores_aristas, width=2)
```

### Elección de layout según el grafo

| Situación | Layout recomendado |
|---|---|
| Grafo general pequeño/mediano | `nx.spring_layout(G, seed=SEED)` |
| Árboles / jerarquías | `nx.bfs_layout(G, start)` o `nx.spring_layout` |
| Grafos bipartitos | `nx.bipartite_layout(B, top)` |
| Ciclos / ruedas | `nx.circular_layout(G)` / `nx.shell_layout(G)` |
| Grafos planares | `nx.planar_layout(G)` (requiere `nx.check_planarity(G)[0] == True`) |
| Grafos dirigidos con capas | `nx.multipartite_layout(G, subset_key="layer")` |

Para grafos interactivos exploratorios (no para el entregable — ver §1.6), usar PyVis:
```python
from pyvis.network import Network
net = Network(notebook=True, cdn_resources="in_line")
net.from_nx(G)
net.show("grafo.html")
```

---

## 4. Plantilla de registro de uso de IA

Copiar y adaptar esta celda Markdown al final de cada ejercicio, según la normativa del departamento sobre uso de IA en boletines evaluables. Sirve igual para Claude Code, ChatGPT, Gemini, GitHub Copilot, etc. — indica cuál se usó en cada caso.

```markdown
### 🤖 Registro de uso de IA

- **Herramienta(s) utilizada(s):** [p. ej. Claude Code (Claude Sonnet 5) / ChatGPT / Gemini / GitHub Copilot — indicar modelo si se conoce]
- **Prompt(s) utilizado(s):**
  1. "..."
  2. "..."
- **Fase del ejercicio en la que se usó IA:**
  [p. ej. planteamiento de la demostración / depuración del código / redacción / verificación]
- **Verificación de no-alucinación realizada:**
  - [ ] Resultado contrastado analíticamente a mano
  - [ ] Resultado contrastado con un caso/ejemplo conocido de la bibliografía
  - [ ] Resultado verificado computacionalmente con una implementación independiente
  - Detalle: "..."
- **Modificaciones realizadas sobre la propuesta de la IA:**
  "..."
- **Declaración de autoría:** El razonamiento matemático y la decisión final han sido
  revisados y comprendidos por el/la estudiante, quien asume la responsabilidad
  del contenido entregado.
```
