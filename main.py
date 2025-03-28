import numpy as np
from Darmanim.window import Window
from Darmanim.draw import rectangle, ellipse, polygon, circle, line

if __name__ == '__main__':
    window = Window(size=(900, 900))

    rectangle(window, (250, 350, 400, 200))
    ellipse(window, (450, 450), 200, 100, stroke=0)
    circle(window, (500, 700), 100)
    line(window, (600, 100), (700, 300))
    polygon(window, [(200, 200), (300, 300), (400, 200)], stroke=3)

    window.run()


    