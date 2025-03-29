from Darmanim.window import Window
from Darmanim.globals import LerpValue
from Darmanim.draw import animated_lines, circle


if __name__ == '__main__':
    window = Window(size=(900, 900), output='triangulation.mp4', record_time=5)

    time = 0.025
    for i in range(10):
        y0 = y1 = 100 + 70*i
        y2 = y3 = y0 + 70
        for j in range(10):
            x0 = x2 = 100 + 70*j
            x1 = x3 = x0 + 70
            start = 10*time*i + time*j + 100*time
            triangle1 = ((x0, y0), (x1, y1), (x2, y2), (x0, y0))
            triangle2 = ((x1, y1), (x2, y2), (x3, y3), (x1, y1))
            radius = LerpValue(0, 5, transition_time=time, start_time=start-100*time)

            circle(window, (x0, y0), radius, stroke=0)
            if i == 9: circle(window, (x0, y2), radius, stroke=0)
            animated_lines(window, triangle1, 'gray', transition_time=time, start_time=start)
            animated_lines(window, triangle2, 'gray', transition_time=time, start_time=start)

        circle(window, (x1, y0), radius, stroke=0)
    circle(window, (x1, y2), radius, stroke=0)

    window.record()
    window.run()