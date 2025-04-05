from Darmanim.window import Window
from Darmanim.polygons import Circle
from Darmanim.graph import Graph, Point, Path, Line


if __name__ == '__main__':
    window = Window(size=(900, 900))

    graph = Graph(size=(800, 800))
    window.add(graph)

    circle_x = Circle((0, 6), 2, color='blue')
    graph.add(circle_x)
    px = graph.add(circle_x.point_along(0, None, transition_time=2))

    circle_y = Circle((6, 0), 2, color='blue')
    graph.add(circle_y)
    py = graph.add(circle_y.point_along(0, None, transition_time=1))

    point = Point(px.x, py.y)
    graph.add(Line(px, point, color='gray'))
    graph.add(Line(py, point, color='gray'))

    graph.add(point)
    graph.add(Path(point, plot_time=2, color='yellow', stroke=3))

    window.run()