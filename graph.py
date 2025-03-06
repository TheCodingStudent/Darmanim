import numpy as np
from Darmanim.window import Window
from Darmanim.graph import Graph, Function

if __name__ == '__main__':
    window = Window(size=(1000, 1000))

    # CREAR GRAFICA
    graph = Graph()

    # AGREGAR GRAFICA A LA VENTANA
    window.add(graph)

    # CREAR FUNCION SENO
    function1 = Function(np.sin)
    graph.add(function1)

    window.start()