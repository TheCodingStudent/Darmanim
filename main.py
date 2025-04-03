import numpy as np
from Darmanim.window import Window
from Darmanim.graph import Graph, Function
from Darmanim.animations import continous_phase


@continous_phase(0, 2*np.pi, 1)
def animated_sine(x: np.array) -> np.array:
    return np.sin(x)


if __name__ == '__main__':
    window = Window(size=(1600, 900), fps=120, output='graph movements.mp4', record_time=8)

    graph = Graph(size=(800, 800))
    window.add(graph)

    graph.add(Function(animated_sine, color='babypink'))

    graph.displace_to(50, graph.y, start_time=1, transition_time=1)
    graph.move_to(5, 0, start_time=3, transition_time=1)
    graph.reshape(1500, 800, start_time=5, transition_time=2)
    graph.displace_to(50, graph.y, start_time=5, transition_time=2)

    window.record()
    window.run()