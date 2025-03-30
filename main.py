from Darmanim.draw import AnimatedText
from Darmanim.window import Window


if __name__ == '__main__':
    window = Window(size=(900, 900))

    darmanim = AnimatedText(window, 'Darmanim <3', 450, 450, 120, anchor_x='centerx', anchor_y='centery', transition_time=2)
    darmanim['<3'].color = 'red'

    window.run()

