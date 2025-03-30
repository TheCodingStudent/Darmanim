from Darmanim.window import Window
from Darmanim.values import LerpValue
from Darmanim.color import LerpColor, Color
from Darmanim.draw import AnimatedLines, Circle, AnimatedLine


if __name__ == '__main__':
    window = Window(size=(0, 0), output='contour lines.mp4', record_time=20, fps=240)
    folder = 'c:/users/angel/desktop/uach/semestre 8/cartografia/modelo cerro del pescadito/darmanim/'

    contour_x = window.width - 900
    contour_y = (window.height - 800) // 2

    time = 0.05
    ty = 50
    start_time = 0
    for y in range(contour_y, 900+contour_y, 100):
        for x in range(contour_x, 900+contour_x, 100):
            color = LerpColor(Color.red, 'white', 10*time, start_time)
            radius = LerpValue(0, 5, time, start_time)
            Circle(window, (x, y), radius, color, stroke=0)

            AnimatedLine(window, (210, ty), (810, ty), 'white', 1, time, start_time)
            ty += 980/81
            start_time += time

    time = 0.05
    for i in range(8):
        y0 = y1 = 100*i + contour_y
        y2 = y3 = y0 + 100
        for j in range(8):
            x0 = x2 = 100*j + contour_x
            x1 = x3 = x0 + 100
            AnimatedLines(window, [(x0, y0), (x1, y1), (x2, y2)], 'gray', True, 1, 4*time, start_time)
            AnimatedLines(window, [(x1, y1), (x2, y2), (x3, y3)], 'gray', True, 1, 4*time, start_time)
            start_time += time

    time = 1.5
    for elevation in range(1575, 1725, 25):
        with open(f'{folder}/{elevation}.txt') as f:
            points = []
            for line in f.readlines():
                x, y, _ = line.split(',')
                points.append((float(x)+contour_x, float(y)+contour_y))

            color = 'brown' if elevation % 100 else 'lightbrown' 
            closed = elevation > 1600
            AnimatedLines(window, points, color, closed, 3, time, start_time)
            start_time += time

    window.run()

