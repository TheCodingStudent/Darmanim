from Darmanim.window import Window
from Darmanim.color import LerpColor
from Darmanim.draw import AnimatedText


if __name__ == '__main__':
    color = LerpColor('red', 'background', 0.5)
    window = Window(size=(900, 900), color=color)

    darmanim = AnimatedText(window, 'Darmanim <3', 450, 450, 120, anchor_x='centerx', anchor_y='centery')
    darmanim['<3'].color = 'red'

    window.run()

