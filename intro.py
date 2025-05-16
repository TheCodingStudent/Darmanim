from Darmanim.window import Window
from Darmanim.draw import Text, AnimatedText


if __name__ == '__main__':
    window = Window(size=(0, 0), fps=120, output='intro.mp4', record_time=5)

    title = AnimatedText(
        surface=window,
        text=['Diseño de curvas'.upper(), 'horizontales simples'.upper()],
        x=window.center[0], y=window.center[1],
        size=100, anchor_x='centerx', anchor_y='centery'
    )

    authors = AnimatedText(
        surface=window,
        text=['Darlenne Gardea', 'Armando Chaparro'],
        x=window.center[0], y=title.rect.bottom + 100,
        size=36, anchor_x='centerx', anchor_y='top',
        start_time=1
    )

    title.displace_by(0, -authors.rect.bottom, start_time=3, transition_time=1)
    authors.displace_by(0, -authors.rect.bottom, start_time=3, transition_time=1)

    window.run()