import math
from Darmanim.window import Window
from Darmanim.color import get_colors
from Darmanim.values import LerpEventGroup
from Darmanim.draw import AnimatedLine, Line, Circle, AnimatedText, AnimatedLines

if __name__ == '__main__':
    window = Window(size=(0, 0), fps=120, output='curve.mp4', record_time=18)

    # VARIABLES DEL PROYECTO
    scale = 3
    y_proy = 65
    GC = 5
    RC = 229.184 * scale
    ST = 229.184 * scale
    PC = window.center[0] - ST * math.cos(math.pi/4), y_proy + ST * math.sin(math.pi/4)

    PSC = [
        (0.000,	  0.000),   (4.351,	  -4.238),
        (19.445,  -17.350), (35.624,  -29.097),
        (52.765,  -39.389), (70.739,  -48.147),
        (89.407,  -55.307), (108.628, -60.811),
        (128.255, -64.620), (148.140, -66.703),
        (168.131, -67.046), (188.075, -65.645),
        (207.822, -62.511), (227.220, -57.668),
        (246.123, -51.152), (264.385, -43.014),
        (281.869, -33.315), (298.441, -22.130),
        (313.975, -9.542),  (324.115, 0.000)
    ]

    PT_PROY = window.center[0] + ST * math.cos(math.pi/4), y_proy - ST * math.sin(math.pi/4)
    PI = (window.center[0], y_proy)
    PT = window.center[0] + ST * math.cos(math.pi/4), y_proy + ST * math.sin(math.pi/4)
    O = PC[0] + ST * math.cos(math.pi/4), PC[1] + ST * math.sin(math.pi/4)

    CORDS = [6.074, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 13.926]
    CORDS = [scale * cord for cord in CORDS]

    ANGLES = [45.75925, 48.26, 50.76, 53.26, 55.76, 58.26, 60.76, 63.26, 65.76, 68.26, 70.76, 73.26, 75.76, 78.26, 80.76, 83.26, 85.76, 88.26, 90]

    # APARECE EL PUNTO DEL PC
    pc = Circle(surface=window, center=PC, radius=0, color='red', stroke=0, z_index=0)
    pc.set_radius(5, transition_time=0.5)
    AnimatedText(surface=window, text='PC', x=PC[0]-10, y=PC[1], size=24, anchor_x='right', anchor_y='centery', transition_time=0.5)

    # UNA LINEA CONECTA EL PC CON EL PI
    pcpi = AnimatedLine(surface=window, start=PC, end=PI, start_time=1)

    # APARECE EL PUNTO DEL PI
    pi = Circle(surface=window, center=PI, radius=0, color='red', stroke=0, z_index=0)
    pi.set_radius(5, start_time=2, transition_time=0.5)
    AnimatedText(surface=window, text='PI', x=PI[0], y=PI[1] - 10, size=24, anchor_x='centerx', anchor_y='bottom', start_time=2, transition_time=0.5)

    # SE DIBUJA UNA LINEA QUE PROYECTA EL PI, DESPUES GIRA Y CONECTA EL PT
    pi_proy = AnimatedLine(surface=window, start=PI, end=(window.center[0]+50, y_proy-50), start_time=2.5, z_index=1)
    pi_proy.rotate(angle=90, start_time=3.5, transition_time=1)
    pi_proy.set_length(ST, start_time=4.5, transition_time=1)
    Line(surface=window, start=PI, end=(window.center[0]+50, y_proy-50), color='gray', start_time=3.5)

    # APARECE LA DEFLEXION
    AnimatedText(surface=window, text='Δ', x=PI[0] + 25, y=PI[1], size=24, anchor_y='centery', start_time=4)

    # APARECE EL PUNTO DEL PT
    pt = Circle(surface=window, center=PT, radius=0, color='red', stroke=0, z_index=0)
    pt.set_radius(5, start_time=5.5, transition_time=0.5)
    AnimatedText(surface=window, text='PT', x=PT[0]+10, y=PT[1], size=24, anchor_y='centery', start_time=5.5, transition_time=0.5)

    # APARECE EL PUNTO DEL ORIGEN Y LINEAS QUE LO CONECTAN
    o = Circle(surface=window, center=O, radius=0, color='red', stroke=0, z_index=0)
    o.set_radius(5, start_time=6, transition_time=1)
    AnimatedLine(surface=window, start=PC, end=O, start_time=6, z_index=1)
    AnimatedLine(surface=window, start=PT, end=O, start_time=6, z_index=1)
    AnimatedText(surface=window, text='O', x=O[0], y=O[1]+10, size=24, anchor_x='centerx', start_time=6)

    rc_y = (O[1] + PC[1]) / 2
    rc_x1 = (O[0] + PC[0]) / 2 - 25
    rc_x2 = (O[0] + PT[0]) / 2 + 25
    AnimatedText(surface=window, text='RC', x=rc_x1, y=rc_y, size=24, anchor_x='centerx', start_time=6)
    AnimatedText(surface=window, text='RC', x=rc_x2, y=rc_y, size=24, anchor_x='centerx', start_time=6)

    # LINEA DEL CL
    AnimatedLine(surface=window, start=PC, end=PT, line_type='dashed', start_time=7)
    AnimatedText(surface=window, text='CL', x=window.center[0]+25, y=PC[1], size=24, anchor_y='centery', start_time=7.5, background='background')

    # DIBUJAR LINEA DE MEDIO ANGULO DE PSC
    deflection_index = 10
    psc_angle = GC * CORDS[deflection_index] / 20

    f = RC * (1 - math.cos(math.radians(psc_angle) / 2))
    psc_angle_length = RC + f
    psc_angle_end = O[0], O[1] - psc_angle_length

    psc_mid_angle_line = AnimatedLine(surface=window, start=O, end=psc_angle_end, color='gray', z_index=2, start_time=8.5)
    psc_mid_angle_line.rotate(angle=psc_angle/2-45)

    # UNIR EL PC CON LA LINEA ANTERIOR
    pc_psc_mid = AnimatedLine(surface=window, start=PC, end=psc_mid_angle_line.end, color='yellow', stroke=2, start_time=9.5)

    # DIBUJAR LINEA DE ANGULO DE PSC
    psc_angle_line = AnimatedLine(surface=window, start=O, end=(O[0], O[1]-RC), color='gray', z_index=2, start_time=10.5)
    psc_angle_line.rotate(angle=psc_angle-45)

    # UNIR EL PC CON LA LINEA ANTERIOR
    d = AnimatedLine(surface=window, start=pc_psc_mid.end, end=psc_angle_line.end, color='red', stroke=2, start_time=11.5)
    c = AnimatedLine(surface=window, start=PC, end=psc_angle_line.end, color='green', stroke=2, start_time=12.5)
    # AnimatedText(surface=window, text='C', x=c.mid[0], y=c.mid[1], size=24)

    # DIBUJAMOS UN CIRCULO EN EL PUNTO SOBRE LA CURVA
    psc = Circle(surface=window, center=psc_angle_line.end, stroke=0, radius=0)
    psc.set_radius(radius=5, start_time=12.5, transition_time=0.25)

    # REMOVEMOS LAS LINEAS Y PUNTO PREVIO (DESPUES SE PUEDE HACER UNA FUNCION QUE HAGA ESTO)
    LerpEventGroup(
        (psc_mid_angle_line, pc_psc_mid, psc_angle_line, c, d, psc),
        ('color', 'color', 'color', 'color', 'color', 'color'),
        get_colors(['gray', 'yellow', 'gray', 'green', 'red', 'white']),
        get_colors(['background', 'white', 'background', 'background', 'background', 'background']),
        transition_time=1, start_time=13.5
    )

    window.remove(psc_mid_angle_line, start_time=14.5)
    window.remove(pc_psc_mid, start_time=14.5)
    window.remove(psc_angle_line, start_time=14.5)
    window.remove(c, start_time=14.5)
    window.remove(d, start_time=14.5)
    window.remove(psc, start_time=14.5)

    # AÑADIMOS LOS PUNTOS SOBRE LA CURVA
    window_psc = []
    for i, (dx, dy) in enumerate(PSC):
        x = PC[0] + dx * scale
        y = PC[1] + dy * scale
        window_psc.append((x, y))
        start_time = 15 + (i+1) / len(PSC)
        psc = Circle(surface=window, center=(x, y), stroke=0, radius=0)
        psc.set_radius(radius=5, start_time=start_time, transition_time=0.25)
        psc.set_radius(radius=3, start_time=16.5, transition_time=0.25)

    AnimatedLines(surface=window, points=window_psc, color='yellow', start_time=17)

    # window.record()
    window.run()