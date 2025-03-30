from Darmanim.draw import Text
from Darmanim.window import Window


if __name__ == '__main__':
    window = Window(size=(900, 900))

    darmanim = Text(window, 'Darm<3anim <3', 50, 400, 100)
    darmanim['a'].color = 'red'

    darmanim['<3'][0].color = 'yellow'

    window.run()

