from Darmanim.graph import Graph
from Darmanim.window import Window, Surface

if __name__ == '__main__':
    window = Window(size=(900, 900), output='surface.mp4', record_time=5)

    surface = Surface(100, 100, (500, 500), color='purple', border_width=1)
    window.add(surface)

    graph = Graph(size=(350, 350))
    surface.add(graph)
    graph.reshape(450, 450, start_time=2, transition_time=1)
    surface.displace_to(200, 200, start_time=1, transition_time=1)

    window.hide(surface, start_time=3)
    window.unhide(surface, start_time=4)

    window.run()