from Darmanim.draw import AnimatedText, Group, Line
from Darmanim.window import Window


if __name__ == '__main__':
    window = Window(size=(0, 0))

    # TITLE
    Line(window, (window.center[0], 0), (window.center[0], window.height))
    Line(window, (0, window.center[1]), (window.width, window.center[1]))

    title = AnimatedText(
        surface=window,
        text=['Curvas de', 'nivel'],
        x=window.center[0], y=window.center[1],
        size=192,
        anchor_x='centerx',
        anchor_y='centery'
    )

    authors = AnimatedText(
        surface=window,
        text='Por Darlenne Gardea y Armando Chaparro',
        x=window.center[0], y=title.rect.bottom,
        size=48,
        anchor_x='centerx',
        anchor_y='top',
        start_time=1
    )

    # Group((title, authors)).displace_by(0, -1000, start_time=3, transition_time=1)

    # POINT CLOUD

    # TRIANGULATION

    window.run()