import numpy as np                          # IMPORT NUMPY TO USE SINE FUNCTION
from Darmanim.time import Clock             # CLOCK WILL BE USED TO USE TIME AS A SINE PHASE
from Darmanim.window import Window          
from Darmanim.graph import Graph, Function


def animated_sine(x: np.array) -> np.array:
    """
    This function returns a sine wave that shifts based on the Darmanim main
    clock time.

    Args:
        x: np.array -> values along the x axis, based on Function configuration

    Returns:
        an np.array with the values of a sine wave with clock used as a phase

    """
    return np.sin(x + Clock.time)


# PROGRAM MAIN
if __name__ == '__main__':
    # CREATE A WINDOW OF 900x900 PIXELS
    window = Window(size=(900, 900))

    # CREATE A GRAPH TO LATER ADD A FUNCTION
    graph = Graph(size=(800, 800))

    # CREATE A FUNCTION AND PASS OUR CUSTOM FUNCTION AS ARGUMENT
    # CALL UPDATE IS TRUE TO UPDATE THE VALUES EACH FRAME
    sine = Function(animated_sine, call_update=True)

    # ADD THE FUNCTION TO THE GRAPH TO SEE IT
    graph.add(sine)

    # ADD THE GRAPH TO THE WINDOW TO BE DISPLAYED. IF COORDINATES ARE NOT SUPPLIED, THEN THE GRAPH WILL BE AT THE CENTER
    window.add(graph)

    # START THE ANIMATION
    window.run()