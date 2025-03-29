import numpy as np
from Darmanim.window import Window
from Darmanim.graph import Graph, Function

if __name__ == '__main__':
    window = Window(size=(900, 900), output='dots.mp4', record_time=7)

    graph = Graph(size=(800, 800))
    window.add(graph)

    sine = Function(np.sin, stroke=3)
    graph.add(sine)

    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'violet']
    for i in range(20):
        color = colors[i%6]
        graph.add(sine.point_along(-7, 7, 10, 0, color, transition_time=2, start_time=0.25*i))

    window.record()
    window.run()

