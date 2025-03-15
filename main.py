import numpy as np
from Darmanim.window import Window
from Darmanim.graph import Graph, Function
from Darmanim.animations import shift_x, shift_y


@shift_y(0, 0.5, 1)
def sine(x: np.array) -> np.array:
    return np.sin(x)


if __name__ == '__main__':
    window = Window(size=(1000, 1000))

    graph = Graph(size=(900, 900))
    window.add(graph)

    function = Function(sine, call_update=True)
    graph.add(function)

    window.run()

