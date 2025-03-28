# IMPORT NUMPY TO USE SINE FUNCTION
import numpy as np
from Darmanim.window import Window
from Darmanim.graph import Graph, Function

# PROGRAM MAIN
if __name__ == '__main__':
    # CREATE A WINDOW OF 900x900 PIXELS
    window = Window(size=(900, 900))

    # CREATE A GRAPH TO LATER ADD A FUNCTION
    graph = Graph(size=(800, 800))

    # CREATE A FUNCTION AND PASS NP.SIN AS ARGUMENT
    sine = Function(np.sin)

    # ADD THE FUNCTION TO THE GRAPH TO SEE IT
    graph.add(sine)

    # ADD THE GRAPH TO THE WINDOW TO BE DISPLAYED. IF COORDINATES ARE NOT SUPPLIED, THEN THE GRAPH WILL BE AT THE CENTER
    window.add(graph)

    # START THE ANIMATION
    window.run()