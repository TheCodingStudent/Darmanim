import numpy as np
from Darmanim.window import Window
from Darmanim.polygons import Circle
from Darmanim.globals import LerpValue, SequenceValue
from Darmanim.graph import Graph, Axis, Grid, Point, Path


if __name__ == '__main__':
    window = Window(size=(950, 950), output='cardioid.mp4', record_time=5)
    # window.not_record()

    grid = Grid(minx=-6, maxx=6, miny=-6, maxy=6)
    graph = Graph(size=(900, 900), grid=grid)
    window.add(graph)
    
    r = 2
    graph.add(Circle((0, 0), r, color='gray'))
    p1 = Circle((0, 0), 2*r).point_along(0, None, transition_time=5)
    c = graph.add(Circle(p1, r, color='gray'))

    p = c.point_along(180, None, transition_time=2.5)
    graph.add(Path(p, color='red', plot_time=5, stroke=3))
    graph.add(p)

    window.run()

