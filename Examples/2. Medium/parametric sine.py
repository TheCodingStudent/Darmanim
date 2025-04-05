import numpy as np
from Darmanim.window import Window
from Darmanim.graph.polygons import Circle
from Darmanim.values import ContinuosValue, LerpEvent
from Darmanim.graph import Graph, Grid, Point, Path, Line


if __name__ == '__main__':
    window = Window(size=(1600, 900), output='sine.mp4', record_time=12.5)

    circle_grid = Grid(x_color=None, y_color=None)
    circle_graph = Graph(size=(500, 500), grid=circle_grid)
    window.add(circle_graph, x=50)

    circle = Circle((0, 0), 1)
    circle_graph.add(circle)
    point = circle.point_along(0, None, transition_time=5)
    circle_graph.add(point)

    sine_grid = Grid(minx=0, maxx=10)
    sine_graph = Graph(size=(950, 500), grid=sine_grid)
    sine_graph.move_to(200*np.pi, 0, start_time=5, transition_time=500)
    window.add(sine_graph, x=600)

    sine_x = ContinuosValue(0, 2*np.pi, 5)
    sine_point = Point(sine_x, point.y, radius=5, stroke=0, color='red')
    sine_graph.add(sine_point)

    sine = Path(sine_point, color='red')
    sine_graph.add(sine)

    line = Line(point, sine_point, color='gray')
    window.add(line)

    LerpEvent(circle, 'radius', 1, 5, transition_time=5, start_time=5, update_element=True)

    window.record()
    
    window.run()