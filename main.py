from Darmanim.window import Window
from Darmanim.graph import Graph

if __name__ == '__main__':
    window = Window(size=(900, 900))

    graph = Graph(size=(800, 800))
    window.add(graph)

    window.run()