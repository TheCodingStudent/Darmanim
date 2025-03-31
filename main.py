import numpy as np
from Darmanim.time import Clock
from Darmanim.window import Window
from Darmanim.graph import Graph, Function


def animated_sine(x: np.array) -> np.array:
    return np.sin(x + Clock.time)


if __name__ == '__main__':
    window = Window(size=(900, 900))
    
    graph = Graph(size=(800, 800))
    window.add(graph)

    function = Function(animated_sine)
    graph.add(function)

    window.run()