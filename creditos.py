from Darmanim.window import Window
from Darmanim.draw import Text, AnimatedText, FastText


if __name__ == '__main__':
    window = Window(size=(0, 0), fps=120, output='creditos.mp4', record_time=11)

    credits = [
        "Dirección General, Programación y Desarrollo Técnico: Armando Chaparro",
        "Diseño de Interfaz, Documentación Técnica y Tutoriales: Armando Chaparro",
        "Gestión del Repositorio y Control de Versiones: Armando Chaparro",
        "Dirección de Arte y Diseño Estético: Darlenne Gardea",
        "Estudio de Mercado y Análisis de Usuario: Darlenne Gardea",
        "Colaboración Creativa y Soporte Generañ: Darlenne Gardea",
        "",
        "Créditos Especiales",
        "A mi Bebe,",
        "por su invaluable apoyo,",
        "por ser el alma detrás del apartado estético de este proyecto,",
        "por inspirarme con su dedicación, creatividad y amor,",
        "por estar a mi lado en los momentos más intensos y también en los más dulces,",
        "y por regalarme otro semestre lleno de cariño, sonrisas y complicidad.",
        "Gracias por hacerme tan feliz y por ser parte de mi vida.",
    ]

    y = window.height
    for line in credits:
        text = FastText(
            surface=window,
            text=line,
            x=window.center[0], y=y,
            anchor_x='centerx', size=48,
            start_time=1
        )

        y += text.height

        endline = FastText(
            surface=window,
            text="",
            x=window.center[0], y=y,
            anchor_x='centerx', size=48
        )

        y += text.height

        displacement = 2 * len(credits) * text.height
        text.displace_by(0, -displacement, start_time=1, transition_time=10)
        endline.displace_by(0, -displacement, start_time=1, transition_time=10)

    window.record()

    window.run()