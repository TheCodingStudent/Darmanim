import random
from Darmanim.window import Window
from Darmanim.values import LerpValue
from Darmanim.color import LerpColor
from Darmanim.draw import AnimatedLines, Circle, AnimatedText, FastText, Polygon, Lines, Rectangle


if __name__ == '__main__':
    window = Window(size=(0, 0), output='contour curves.mp4', record_time=30)

    top = AnimatedText(window, 'Curvas de nivel', window.width/2, window.height/2, 200, 'white', anchor_x='centerx', anchor_y='bottom')
    AnimatedText(window, 'Armando Chaparro & Darlenne Gardea', window.width/2, top.rect.bottom, 50, 'white', anchor_x='centerx')

    height = LerpValue(0, window.height, 0.5, 2)
    Rectangle(window, (0, 0, window.width, height), 'background', 0)
    start_time = 3.5

    folder = 'c:/users/angel/desktop/uach/semestre 8/cartografia/modelo cerro del pescadito/darmanim/'

    contour_x = window.width - 900
    contour_y = (window.height - 800) // 2

    tx, ty = 100, 50
    i = 1

    for y in range(contour_y, 900+contour_y, 100):
        for x in range(contour_x, 900+contour_x, 100):

            time = 0.025 if i > 9 else 0.5
            color_time = 10*time if i > 9 else time
            color = 'white' if i > 9 else LerpColor('red', 'white', color_time, start_time)
            radius = 5 if i > 9 else LerpValue(0, 5, time/4, start_time)

            Circle(window, (x, y), radius, color, stroke=0, start_time=start_time, z_index=0)
            FastText(window, f'{random.randint(1575, 1700)}', x+10, y-10, 16, anchor_y='bottom', start_time=start_time, z_index=1)

            number = None
            if i > 9:
                number = FastText(window, f'{i:<2}', tx, ty, 24, 'red', start_time=start_time)
                text = FastText(window, f': {x:.2f}, {y:.2f}', *number.rect.topright, 24, start_time=start_time)
            else:
                text = AnimatedText(window, f'{i:<2}: {x:.2f}, {y:.2f}', tx, ty, 24, transition_time=time, start_time=start_time)
                text[:2].color = 'red'

            ty += text.rect.height
            if ty >= 1030:
                ty = 50
                tx += text.rect.width + 100
                if number: tx += number.rect.width

            i += 1
            start_time += time

    time = 0.05
    for i in range(8):
        y0 = y1 = 100*i + contour_y
        y2 = y3 = y0 + 100
        for j in range(8):
            x0 = x2 = 100*j + contour_x
            x1 = x3 = x0 + 100
            AnimatedLines(window, [(x0, y0), (x1, y1), (x2, y2)], 'gray', True, 1, 4*time, start_time, z_index=1)
            AnimatedLines(window, [(x1, y1), (x2, y2), (x3, y3)], 'gray', True, 1, 4*time, start_time, z_index=1)
            start_time += time

    start_time += 1
    time = 1.5

    square = [(contour_x, contour_y), (contour_x, 800+contour_y), (800+contour_x, 800+contour_y), (800+contour_x, contour_y)]
    AnimatedLines(window, square, 'red', True, 3, time, start_time)
    Polygon(window, square, LerpColor(window.color, 'red', 0.1, start_time+time), 0, start_time)

    hide_time = time
    hide_color = LerpColor('red', window.color, hide_time, start_time=start_time+time+hide_time)
    Polygon(window, square, color=hide_color, stroke=0, start_time=start_time+time+hide_time)

    start_time += time

    colors = ['yellow', 'green', 'blue', 'purple', 'violet', 'red']
    current_color = 'red'
    z_index = 100

    for elevation in range(1575, 1725, 25):
        with open(f'{folder}/{elevation}.txt') as f:
            points = []
            for line in f.readlines():
                x, y, _ = line.split(',')
                points.append((float(x)+contour_x, float(y)+contour_y))

            if elevation == 1575:
                points.append((800+contour_x, contour_y))
                points.append((contour_x, contour_y))
            elif elevation == 1600:
                points.append((contour_x, contour_y))

            AnimatedLines(window, points, colors[0], True, 3, start_time=start_time, z_index=z_index-1)

            pol_color = LerpColor(current_color, colors[0], 0.1, start_time=start_time+time)
            Polygon(window, points, color=pol_color, stroke=0, start_time=start_time+0.1, z_index=z_index)

            hide_color = LerpColor(colors[0], window.color, 2*hide_time, start_time=start_time+time+hide_time)
            Polygon(window, points, color=hide_color, stroke=0, start_time=start_time+time+hide_time, z_index=z_index)

            color = 'brown' if elevation % 100 else 'lightbrown' 
            Lines(window, points, LerpColor(colors[0], color, 0.5, 24.5+3*time), True, 3, start_time=24.5+3*time, z_index=2)

            current_color = colors.pop(0)
            z_index -= 1

            start_time += time
    
    start_time += 3 * time

    h = LerpValue(0, 1000, 0.1, start_time=start_time)
    Rectangle(window, (100, 50, 800, h), window.color, 0)

    window.run()