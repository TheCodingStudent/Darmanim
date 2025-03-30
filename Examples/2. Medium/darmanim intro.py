from Darmanim.window import Window
from Darmanim.color import LerpColor
from Darmanim.values import LerpValue, SequenceValue
from Darmanim.draw import Text, Line, AnimatedLines, Circle, Rectangle, Ellipse, RegularPolygon

if __name__ == '__main__':
    window = Window(size=(900, 900))

    Line(window, (450, 0), (450, 900), 'black')

    anchor = {'anchor_x': 'centerx', 'anchor_y': 'centery'}
    darmanim = Text(window, 'Darmanim <3', 450, 450, 120, **anchor)

    colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'violet']
    for i, color in enumerate(colors):
        darmanim[i].color = LerpColor('white', color, 0.1, 0.1*i)

    darmanim[-2:].color = LerpColor('white', 'red', 0.1, 0.8)

    points = ((100, 100), (200, 200), (300, 100), (300, 400))
    AnimatedLines(window, points, stroke=3)

    Circle(window, (100, 700), SequenceValue((50, 100, 50), 2))

    Rectangle(window, (600, 600, 100, LerpValue(100, 200, 1)), stroke=0)

    Ellipse(window, (600, 200), SequenceValue((100, 200, 100), 2), 50)

    RegularPolygon(window, (300, 600), 100, LerpValue(3, 10, 2))

    window.run()