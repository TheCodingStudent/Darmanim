from Darmanim.window import Window
from Darmanim.draw import animated_rect, animated_line

if __name__ == '__main__':
    window = Window(size=(900, 900))

    animated_rect(window, (250, 50, 400, 800), 'black', 5, 0.5)
    animated_line(window, (450, 100), (450, 850), 'black', 5, 0.125, 0.5)
    animated_line(window, (250, 100), (650, 100), 'black', 5, 0.125, 0.5)

    line_time = 0.0625
    for i in range(20):
        y = 100 + 37.5*i
        animated_line(window, (250, y), (650, y), 'black', 2, line_time, 0.625+i*line_time)

    window.run()