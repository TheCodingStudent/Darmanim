from Darmanim.plot import Plot
from Darmanim.window import Window


if __name__ == '__main__':
    window = Window(size=(1000, 1000))

    plot = Plot(size=(900, 900))
    plot.plot(((-5, 5), (5, 5), (5, -5), (-5, -5)))
    window.add(plot)

    window.run()

