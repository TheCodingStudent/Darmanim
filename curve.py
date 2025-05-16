import math
from Darmanim.window import Window, Surface
from Darmanim.draw import AnimatedLine, Line, Circle, AnimatedText, AnimatedLines
from Darmanim.draw.table import Table

if __name__ == '__main__':
    window = Window(size=(0, 0), fps=120, output='curve.mp4', record_time=24)

    main_surface = Surface(*window.center, size=(1080, 1080), anchor_x='centerx', anchor_y='centery')
    window.add(main_surface)

    # VARIABLES DEL PROYECTO
    scale = 3
    y_proy = 65
    GC = 5
    RC = 229.184 * scale
    ST = 229.184 * scale
    PC = main_surface.center[0] - ST * math.cos(math.pi/4), y_proy + ST * math.sin(math.pi/4)

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

    PT_PROY = main_surface.center[0] + ST * math.cos(math.pi/4), y_proy - ST * math.sin(math.pi/4)
    PI = (main_surface.center[0], y_proy)
    PT = main_surface.center[0] + ST * math.cos(math.pi/4), y_proy + ST * math.sin(math.pi/4)
    O = PC[0] + ST * math.cos(math.pi/4), PC[1] + ST * math.sin(math.pi/4)

    CORDS = [6.074, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 13.926]
    CORDS = [scale * cord for cord in CORDS]

    ANGLES = [45.75925, 48.26, 50.76, 53.26, 55.76, 58.26, 60.76, 63.26, 65.76, 68.26, 70.76, 73.26, 75.76, 78.26, 80.76, 83.26, 85.76, 88.26, 90]

    # APARECE EL PUNTO DEL PC
    pc = Circle(surface=main_surface, center=PC, radius=0, color='red', stroke=0, z_index=0)
    pc.set_radius(5, transition_time=0.5)
    AnimatedText(surface=main_surface, text='PC', x=PC[0]-10, y=PC[1], size=24, anchor_x='right', anchor_y='centery', transition_time=0.5)

    # UNA LINEA CONECTA EL PC CON EL PI
    pcpi = AnimatedLine(surface=main_surface, start=PC, end=PI, start_time=1)

    # APARECE EL PUNTO DEL PI
    pi = Circle(surface=main_surface, center=PI, radius=0, color='red', stroke=0, z_index=0)
    pi.set_radius(5, start_time=2, transition_time=0.5)
    AnimatedText(surface=main_surface, text='PI', x=PI[0], y=PI[1] - 10, size=24, anchor_x='centerx', anchor_y='bottom', start_time=2, transition_time=0.5)

    # SE DIBUJA UNA LINEA QUE PROYECTA EL PI, DESPUES GIRA Y CONECTA EL PT
    pi_proy = AnimatedLine(surface=main_surface, start=PI, end=(main_surface.center[0]+50, y_proy-50), start_time=2.5, z_index=1)
    pi_proy.rotate(angle=90, start_time=3.5, transition_time=1)
    pi_proy.set_length(ST, start_time=4.5, transition_time=1)
    Line(surface=main_surface, start=PI, end=(main_surface.center[0]+50, y_proy-50), color='gray', start_time=3.5)

    # APARECE LA DEFLEXION
    AnimatedText(surface=main_surface, text='Δ', x=PI[0] + 25, y=PI[1], size=24, anchor_y='centery', start_time=4)

    # APARECE EL PUNTO DEL PT
    pt = Circle(surface=main_surface, center=PT, radius=0, color='red', stroke=0, z_index=0)
    pt.set_radius(5, start_time=5.5, transition_time=0.5)
    AnimatedText(surface=main_surface, text='PT', x=PT[0]+10, y=PT[1], size=24, anchor_y='centery', start_time=5.5, transition_time=0.5)

    st_1_x = (PI[0] + PC[0]) / 2
    st_2_x = (PT[0] + PI[0]) / 2
    st_y = (PC[1] + PI[1]) / 2
    AnimatedText(surface=main_surface, text='ST', x=st_1_x, y=st_y, size=24, anchor_x='right', anchor_y='bottom', start_time=5.5, transition_time=0.5)
    AnimatedText(surface=main_surface, text='ST', x=st_2_x, y=st_y, size=24, anchor_x='left', anchor_y='bottom', start_time=5.5, transition_time=0.5)

    # APARECE EL PUNTO DEL ORIGEN Y LINEAS QUE LO CONECTAN
    o = Circle(surface=main_surface, center=O, radius=0, color='red', stroke=0, z_index=0)
    o.set_radius(5, start_time=6, transition_time=1)
    AnimatedLine(surface=main_surface, start=PC, end=O, start_time=6, z_index=1)
    AnimatedLine(surface=main_surface, start=PT, end=O, start_time=6, z_index=1)
    AnimatedText(surface=main_surface, text='O', x=O[0], y=O[1]+10, size=24, anchor_x='centerx', start_time=6)

    rc_y = (O[1] + PC[1]) / 2
    rc_x1 = (O[0] + PC[0]) / 2 - 25
    rc_x2 = (O[0] + PT[0]) / 2 + 25
    AnimatedText(surface=main_surface, text='RC', x=rc_x1, y=rc_y, size=24, anchor_x='centerx', start_time=6)
    AnimatedText(surface=main_surface, text='RC', x=rc_x2, y=rc_y, size=24, anchor_x='centerx', start_time=6)

    # LINEA DEL CL
    AnimatedLine(surface=main_surface, start=PC, end=PT, line_type='dashed', start_time=7)
    AnimatedText(surface=main_surface, text='CL', x=main_surface.center[0]+25, y=PC[1], size=24, anchor_y='centery', start_time=7.5, background='background')

    # DIBUJAR LINEA DE MEDIO ANGULO DE PSC
    deflection_index = 10
    psc_angle = GC * CORDS[deflection_index] / 20

    f = RC * (1 - math.cos(math.radians(psc_angle) / 2))
    psc_angle_length = RC + f
    psc_angle_end = O[0], O[1] - psc_angle_length

    psc_mid_angle_line = AnimatedLine(surface=main_surface, start=O, end=psc_angle_end, color='gray', z_index=2, start_time=8.5)
    psc_mid_angle_line.rotate(angle=psc_angle/2-45)

    # UNIR EL PC CON LA LINEA ANTERIOR
    pc_psc_mid = AnimatedLine(surface=main_surface, start=PC, end=psc_mid_angle_line.end, color='red', stroke=2, start_time=9.5)

    # DIBUJAR LINEA DE ANGULO DE PSC
    psc_angle_line = AnimatedLine(surface=main_surface, start=O, end=(O[0], O[1]-RC), color='gray', z_index=2, start_time=10.5)
    psc_angle_line.rotate(angle=psc_angle-45)

    # UNIR EL PC CON LA LINEA ANTERIOR
    d = AnimatedLine(surface=main_surface, start=pc_psc_mid.end, end=psc_angle_line.end, color='red', stroke=2, start_time=11.5)
    c = AnimatedLine(surface=main_surface, start=PC, end=psc_angle_line.end, color='green', stroke=2, start_time=12.5)
    # AnimatedText(surface=main_surface, text='C', x=c.mid[0], y=c.mid[1], size=24)

    # DIBUJAMOS UN CIRCULO EN EL PUNTO SOBRE LA CURVA
    psc = Circle(surface=main_surface, center=psc_angle_line.end, stroke=0, radius=0)
    psc.set_radius(radius=5, start_time=12.5, transition_time=0.25)
    psc.set_radius(radius=0, start_time=13.5, transition_time=0.5)

    # AÑADIMOS LOS PUNTOS SOBRE LA CURVA
    window_psc = []
    for i, (dx, dy) in enumerate(PSC):
        x = PC[0] + dx * scale
        y = PC[1] + dy * scale
        window_psc.append((x, y))
        start_time = 15 + (i+1) / len(PSC)
        if i % 2 == 0: continue
        psc = Circle(surface=main_surface, center=(x, y), stroke=0, radius=0)
        psc.set_radius(radius=5, start_time=start_time, transition_time=0.25)
        psc.set_radius(radius=3, start_time=16.5, transition_time=0.25)

    AnimatedLines(surface=main_surface, points=window_psc, color='yellow', stroke=2, start_time=17, z_index=float('inf'))

    # AÑADIMOS TEXTOS PARA LOS NUEVOS ELEMENTOS GEOMETRICOS
    left_rc_mid = (PC[0] + O[0]) / 2, (PC[1] + O[1]) / 2
    angle_mid = left_rc_mid[0] + 65, left_rc_mid[1] - 65
    AnimatedLine(surface=main_surface, start=left_rc_mid, end=angle_mid, color='darkyellow', start_time=18)
    AnimatedText(surface=main_surface, text='Θ', x=(left_rc_mid[0] + angle_mid[0])/2, y=(left_rc_mid[1] + angle_mid[1])/2, size=24, start_time=18)

    AnimatedLine(surface=main_surface, start=(O[0], PC[1]), end=(O[0], 350), color='gray', start_time=19)
    AnimatedText(surface=main_surface, text='M', x=O[0], y=(PC[1]+350)/2, size=24, anchor_x='centerx', anchor_y='centery', background='background', start_time=19.5, transition_time=0.25)
    AnimatedLine(surface=main_surface, start=(O[0], 350), end=PI, color='gray', start_time=20)
    AnimatedText(surface=main_surface, text='E', x=O[0], y=(PI[1]+350)/2, size=24, anchor_x='centerx', anchor_y='centery', background='background', start_time=20.5, transition_time=0.25)

    right_rc_mid = (PT[0] + O[0]) / 2, (PT[1] + O[1]) / 2
    chaining_line = AnimatedLine(surface=main_surface, start=O, end=window_psc[-3], color='gray', start_time=21)
    chaining_dim = AnimatedLine(surface=main_surface, start=right_rc_mid, end=chaining_line.mid, color='darkyellow', start_time=22)
    AnimatedText(surface=main_surface, text='20m', x=chaining_dim.mid[0]-5, y=chaining_dim.mid[1], size=24, anchor_y='bottom', start_time=23, transition_time=0.25)

    # DESPLAZAMOS LA VENTANA PARA HACER ESPACIO
    main_surface.displace_to(x=20, y=0, start_time=15, transition_time=2)

    # CREAMOS LA TABLA DE VALORES
    VALUES = [
        ["Estaciones", "Cuerdas", "Deflexiones", "Azimut", "X", "Y"],
        [7053.926,	0,	    '''0°0'0"''',	    '''45°0'0"''',	    473.827,	551.172],
        [7060,	    6.074,	'''0°45'33.3"''',	'''45°45'33.3"''',	478.178,	546.934],
        [7080,	    20,	    '''2°30'0"''',      '''48°15'33.3"''',  493.272,	533.822],
        [7100,	    20,	    '''2°30'0"''',      '''50°45'33.3"''',  509.451,	522.075],
        [7120,	    20,	    '''2°30'0"''',      '''53°15'33.3"''',  526.592,	511.783],
        [7140,	    20,	    '''2°30'0"''',      '''55°45'33.3"''',  44.5655,	503.024],
        [7160,	    20,	    '''2°30'0"''',      '''58°15'33.3"''',  63.2335,	495.865],
        [7180,	    20,	    '''2°30'0"''',      '''60°45'33.3"''',  82.4545,	490.360],
        [7200,	    20,	    '''2°30'0"''',      '''63°15'33.3"''',  2.08210,	486.552],
        [7220,	    20,	    '''2°30'0"''',      '''65°45'33.3"''',  21.9670,  	484.468],
        [7240,	    20,	    '''2°30'0"''',      '''68°15'33.3"''',  41.9578, 	484.126],
        [7260,	    20,	    '''2°30'0"''',      '''70°45'33.3"''',  61.9024, 	485.527],
        [7280,	    20,	    '''2°30'0"''',      '''73°15'33.3"''',  81.6490, 	488.661],
        [7300,	    20,	    '''2°30'0"''',      '''75°45'33.3"''',  1.04720, 	493.504],
        [7320,	    20,	    '''2°30'0"''',      '''78°15'33.3"''',  19.9496, 	500.019],
        [7340,	    20,	    '''2°30'0"''',      '''80°45'33.3"''',  38.2121, 	508.157],
        [7360,	    20,	    '''2°30'0"''',      '''83°15'33.3"''',  55.6959,  	517.856],
        [7380,	    20,	    '''2°30'0"''',      '''85°45'33.3"''',  72.2679, 	529.042],
        [7400,	    20,	    '''2°30'0"''',      '''88°15'33.3"''',  87.8018, 	541.629],
        [7413.926,	13.926,	'''1°44'26.7"''',   '''90°0'0"''',  	797.942,	551.172]
    ]

    table = Table(
        surface=window, title='CURVA HORIZONTAL SIMPLE'.title(),
        x=1120, y=40, width=750, height=1000, size=24,
        columns=len(VALUES[0]), rows=len(VALUES), start_time=17
    )

    for i, row in enumerate(VALUES):
        for j, value in enumerate(row):
            table.set_value(column=j, row=i, value=str(value).title())

    window.record()
    window.run()