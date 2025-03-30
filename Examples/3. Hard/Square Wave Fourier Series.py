import numpy as np
from Darmanim.window import Window
from Darmanim.polygons import Circle
from Darmanim.values import ContinuosValue
from Darmanim.graph import Graph, Grid, Point, Path, BlankGrid, BlankGraph, Function

def square_wave(x: np.array) -> np.array:
    y = x / (np.pi)
    y = y.astype(np.int64)
    y = 2 * (y % 2) - 1
    y[x < 0] *= -1
    return -y

def create_graph(window: Window, n: int) -> None:
    colors = ['blue', 'green', 'yellow', 'purple', 'red', 'blue', 'green', 'yellow', 'purple']

    n_grid = Grid(miny=-1.5, maxy=1.5, minx=-2*np.pi, maxx=2*np.pi)
    n_graph = Graph(size=(1500, 200), grid=n_grid)
    n_graph.shift(200*np.pi, 0, 1000, start_time=5)
    c_graph = BlankGraph(size=(200, 200), border_width=0, grid=BlankGrid.square(1.5))
    
    center = (0, 0)
    for k in range(1, n+1):
        color = colors[k-1]
        period = 2*k - 1
        radius = 4/(np.pi * period)

        c = Circle(center, radius, color=color)
        center = c.point_along(0, None, color, radius=5, stroke=0, transition_time=5/period)
        c_graph.add(c, center)

    n_graph.add(Function(square_wave, color='gray'))

    p = Point(ContinuosValue(-2*np.pi, 2*np.pi, 5), center.y)
    n_graph.add(p, Path(p, color=color, stroke=3))

    m = (n - 1) / 2
    window.add(c_graph, x=50, y=20 + 240*m)
    window.add(n_graph, x=300, y=20 + 240*m)
    window.add(center.line_to_point(p))


if __name__ == '__main__':
    window = Window(output='square wave.mp4', record_time=15)
    create_graph(window, n=1)
    create_graph(window, n=3)
    create_graph(window, n=5)
    create_graph(window, n=7)
    window.run()


    