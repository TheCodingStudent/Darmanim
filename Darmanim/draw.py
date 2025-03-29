import math
import pygame
import pygame.gfxdraw
from Darmanim.window import Window
from Darmanim.color import get_color
from Darmanim.globals import get_value, get_values, Value, LerpValue

type pixel = float
type rect = tuple[pixel, pixel, pixel, pixel]
type coordinate = tuple[pixel, pixel]


def calculate_points(x0: Value, y0: Value, x1: Value, y1: Value, stroke: Value) -> list[pygame.Vector2]:
    start = pygame.Vector2(x0.get(), y0.get())
    end = pygame.Vector2(x1.get(), y1.get())

    direction = (end - start).normalize()
    normal = direction.rotate(-90) * stroke.get(int) / 2

    a = start + normal
    b = end + normal
    c = end - normal
    d = start - normal

    return (a, b, c, d)


def line(window: Window, start: coordinate, end: coordinate, color: any='white', stroke: pixel=1) -> None:
    x0, y0 = get_values(start)
    x1, y1 = get_values(end)
    stroke = get_value(stroke)
    color = get_color(color)

    if isinstance(stroke, Value) and stroke == 1:
        return window.functions.append({
            'function': pygame.draw.aaline,
            'kwargs': {
                'surface': window.screen,
                'color': color,
                'start_pos': (x0, y0),
                'end_pos': (x1, y1)
            },
            'update_kwargs': {
                'color': lambda : color.rgb(),
                'start_pos': lambda : (x0.get(), y0.get()),
                'end_pos': lambda : (x1.get(), y1.get()),
            }
        })

    return window.functions.append({
        'function': pygame.gfxdraw.filled_polygon,
        'args': [window.screen, calculate_points(x0, y0, x1, y1, stroke), color],
        'update_args': [None, lambda: calculate_points(x0, y0, x1, y1, stroke), lambda: color.rgb()]
    })


def lines(window: Window, points: list[coordinate], color: any='white', stroke: pixel=1) -> None:
    color = get_color(color)
    stroke = get_value(stroke)
    top, bottom = [], []

    for p1, p2 in zip(points[:-1], points[1:]):
        x0, y0 = get_values(p1)
        x1, y1 = get_values(p2)

        a, b, c, d = calculate_points(x0, y0, x1, y1, stroke)
        top.extend((a, b))
        bottom.extend((d, c))

    if isinstance(stroke, Value) and stroke == 1:
        return window.functions.append({
            'function': pygame.draw.aalines,
            'kwargs': {
                'surface': window.screen,
                'color': color,
                'closed': False,
                'points': points
            },
            'update_kwargs': {
                'color': lambda: color.rgb()
            }
        })

    window.functions.append({
        'function': pygame.gfxdraw.aapolygon,
        'args': [window.screen, top + bottom[::-1], color],
        'update_args': [None, None, lambda: color.rgb()]
    })

    window.functions.append({
        'function': pygame.gfxdraw.filled_polygon,
        'args': [window.screen, top + bottom[::-1], color],
        'update_args': [None, None, lambda: color.rgb()]
    })


def circle(window: Window, center: coordinate, radius: pixel, color: any='white', stroke: pixel=1) -> None:    
    x, y = get_values(center)
    radius = get_value(radius)
    stroke = get_value(stroke)
    color = get_color(color)

    if isinstance(stroke, Value) and stroke == 1 and type(radius) == Value:
        return window.functions.append({
            'function': pygame.gfxdraw.aacircle,
            'args': [window.screen, x, y, radius, color],
            'update_args': [None, lambda: x.get(), lambda: y.get(), lambda: radius.get(), lambda: color.rgb()]
        })

    return window.functions.append({
        'function': pygame.draw.circle,
        'kwargs': {
            'surface': window.screen,
            'color': color,
            'center': (x, y),
            'radius': radius,
            'width': stroke
        },
        'update_kwargs': {
            'color': lambda: color.rgb(),
            'center': lambda: (x.get(), y.get()),
            'radius': lambda: radius.get(),
            'width': lambda: stroke.get(int)
        }
    })


def ellipse(window: Window, center: coordinate, rx: pixel, ry: pixel, color: any='white', stroke: pixel=1) -> None:
    x, y = get_values(center)
    rx, ry = get_value(rx), get_value(ry)
    stroke = get_value(stroke)
    color = get_color(color)

    if isinstance(stroke, Value) and stroke == 1:
        return window.functions.append({
            'function': pygame.gfxdraw.aaellipse,
            'args': [window.screen, x, y, rx, ry, color],
            'update_args': [None, lambda: x.get(), lambda: y.get(), lambda: rx.get(), lambda: ry.get(), lambda: color.rgb()]
        })

    return window.functions.append({
        'function': pygame.draw.ellipse,
        'kwargs': {
            'surface': window.screen,
            'color': color,
            'rect': (x, y, rx, ry),
            'width': stroke
        },
        'update_kwargs': {
            'color': lambda: color.rgb(),
            'rect': lambda: (x.get()-rx.get(), y.get()-ry.get(), 2*rx.get(), 2*ry.get()),
            'width': lambda: stroke.get(int)
        }
    })


def rectangle(window: Window, rectangle: rect, color: any='white', stroke: pixel=1) -> None:
    x0, y0, x1, y1 = get_values(rectangle)
    color = get_color(color)
    stroke = get_value(stroke)

    return window.functions.append({
        'function': pygame.draw.rect,
        'kwargs': {
            'surface': window.screen,
            'color': color,
            'rect': (x0, y0, x1, y1),
            'width': stroke
        },
        'update_kwargs': {
            'color': lambda: color.rgb(),
            'rect': lambda: (x0.get(), y0.get(), x1.get(), y1.get()),
            'width': lambda: stroke.get(int)
        }
    })


def polygon(window: Window, points: list[coordinate], color: any='white', stroke: pixel=1) -> None:
    color = get_color(color)
    stroke = get_value(stroke)

    if isinstance(stroke, Value) and stroke == 1:
        return window.functions.append({
            'function': pygame.gfxdraw.aapolygon,
            'args': [window.screen, points, color],
            'update_args': [None, None, lambda: color.rgb()]
        })
    
    return window.functions.append({
        'function': pygame.draw.polygon,
        'kwargs': {
            'surface': window.screen,
            'color': color,
            'points': points,
            'width': stroke
        },
        'update_kwargs': {
            'color': lambda: color.rgb(),
            'width': lambda: stroke.get(int)
        }
    })


def animated_line(window: Window, start: coordinate, end: coordinate, color: any='white', stroke: pixel=1, transition_time: float=1, start_time: float=0) -> None:
    x0, y0 = get_values(start)
    x1, y1 = get_values(end)
    color = get_color(color)
    t = LerpValue(0, 1, transition_time, start_time)

    def draw_line() -> None:
        if t.get() == 0: return
        x = x0.lerp(x1, t.get())
        y = y0.lerp(y1, t.get())
        pygame.draw.line(window.screen, color.rgb(), (x0, y0), (x, y))

    return window.functions.append({'function': draw_line})


def animated_lines(window: Window, points: list[coordinate], color: any='white', stroke: pixel=1, transition_time: float=1, start_time: float=0) -> None:
    length = 0
    lengths = []

    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        dist = math.hypot(x1 - x0, y1 - y0)
        lengths.append(dist)
        length += dist

    for i in range(len(points)-1):
        start, end = points[i], points[i+1]
        t = transition_time * lengths[i] / length
        animated_line(window, start, end, color, stroke, t, start_time)
        start_time += t







