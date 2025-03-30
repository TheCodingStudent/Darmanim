import numpy as np
from Darmanim.window import Window
from Darmanim.animations import draw
from Darmanim.values import LerpValue
from Darmanim.graph import Graph, Function


@draw(animation_time=2, start_time=1.5)
def animated_sine(x: np.array) -> np.array:
    return np.sin(x)


if __name__ == '__main__':
    window = Window(size=(900, 900), record_time=10, output='moving sine.mp4')

    graph = Graph(size=(800, 800))
    graph.shift(100, 0, 100, start_time=3.5)
    window.add(graph, y=LerpValue(900, 50, 1))

    function = Function(animated_sine)
    graph.add(function)

    window.record()
    window.run()