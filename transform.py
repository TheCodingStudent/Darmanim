from Darmanim.window import Window
from Darmanim.polygons import Circle, Rectangle
from Darmanim.animation import transform


if __name__ == '__main__':
    window = Window(size=(1000, 1000))
    circle = Circle(x=500, y=500, radius=100, color='pink')
    rectangle = Rectangle(x=500, y=500, w=800, h=400, color='green')

    window.add(
        # fadeOut(
            transform(
                circle,
                rectangle,
                transition_time='0:01',
                start_time='0:01'
            )
            # transition_time='0:01',
            # start_time='0:02'
        # )

    )

    window.start()
