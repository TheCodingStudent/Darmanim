import numpy as np
from Darmanim.graph import Graph, Function
from Darmanim.window import Window, Surface
from Darmanim.plot import Plot, PlotPoint
from Darmanim.animations import continous_phase


@continous_phase(0, 2*np.pi, 1)
def animated_sine(x: np.array) -> np.array:
    return np.sin(x)


if __name__ == '__main__':
    window = Window(size=(1600, 900), fps=120, output='movement.mp4', record_time=5)

    graph_surface = Surface(100, 100, (500, 500), color='purple', border_width=1)
    graph_surface.displace_to(200, 200, start_time=1, transition_time=1)
    window.add(graph_surface)

    graph = Graph(size=(350, 350))
    graph_surface.add(graph)
    graph.add(Function(animated_sine, color='yellow', stroke=3))
    graph.reshape(450, 450, start_time=2, transition_time=1)

    plot_surface = Surface(800, 200, (500, 500), color='black', border_width=1)
    window.add(plot_surface)

    plot = Plot(size=(400, 400))
    plot_point = PlotPoint(color='yellow', radius=5)
    plot.plot(((3, 2), (-1, 5), (0, -3)), plot_style=plot_point, stroke=3)
    plot_surface.add(plot)

    plot.displace_to(25, 25, start_time=1, transition_time=1)
    plot.move_to(3, 1, start_time=2, transition_time=1)
    plot.reshape(450, 450, start_time=3, transition_time=1)
    plot.displace_to(25, 25, start_time=3, transition_time=1)

    window.run()