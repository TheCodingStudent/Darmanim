from Darmanim.graph import Graph
from Darmanim.window import Window
from Darmanim.polygons import Polygon


if __name__ == '__main__':
    window = Window(size=(900, 900), record_time=6, output='moving graph.mp4')

    graph = Graph(size=(800, 800))

    points = [(0, 5), (5, 0), (0, -5), (-5, 0)]
    graph.add(Polygon(points))

    graph.center_at(*points[0], 1, 1)
    graph.center_at(*points[1], 1, 2)
    graph.center_at(*points[2], 1, 3)
    graph.center_at(*points[3], 1, 4)
    graph.center_at(0, 0, 1, 5)

    window.add(graph)

    window.record()
    window.run()