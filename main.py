from Darmanim.graph import Graph
from Darmanim.window import Window


if __name__ == '__main__':
    window = Window(size=(900, 900))

    graph = Graph(size=(800, 800))
    window.add(graph)

    window.run()