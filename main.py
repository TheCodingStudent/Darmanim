from Darmanim.draw import AnimatedLines
from Darmanim.window import Window


if __name__ == '__main__':
    window = Window(size=(1000, 1000))

    time = 0.1
    start_time = 0
    for i in range(9):
        y0 = y1 = 100*i + 50
        y2 = y3 = y0 + 100
        for j in range(9):
            x0 = x2 = 100*j + 50
            x1 = x3 = x0 + 100
            AnimatedLines(window, [(x0, y0), (x1, y1), (x2, y2)], 'gray', True, 1, 8*time, start_time)
            AnimatedLines(window, [(x1, y1), (x2, y2), (x3, y3)], 'gray', True, 1, 8*time, start_time)
            start_time += time

    window.run()

