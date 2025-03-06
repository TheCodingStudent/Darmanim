from __future__ import annotations
import numpy as np
from typing import Any

from Darmanim.globals import Object, color


def get_color(color: Color|str) -> Color|None:
    if color is None: return None
    if color == '': return Color()
    if isinstance(color, str): return getattr(Color, color.upper())
    return color.copy()


def color_lerp(start: color, end: color, t: float) -> color:
    start = np.array(start)
    end = np.array(end)

    (r, g, b, a) = start + (end - start) * t
    return int(r), int(g), int(b), int(a)


class Color:
    def __init__(self, *value: Any):
        if not value: value = (0, 0, 0)
        elif len(value) == 1: value = value[0]

        self.a = 255
        if isinstance(value, (tuple, list)) and len(value) >= 3:
            self.r = value[0]
            self.g = value[1]
            self.b = value[2]
            if len(value) == 4: self.a = value[3]
        elif isinstance(value, str) and value.startswith('#'):
            self.r = int(value[1:3], base=16)
            self.g = int(value[3:5], base=16)
            self.b = int(value[5:7], base=16)
            if len(value) == 9: self.a = int(value[7:9], base=16)
        elif value is None:
            self.r = 0
            self.g = 0
            self.b = 0
    
    def update_alpha(self, alpha: int|float) -> None:
        self.a = alpha

    def copy(self) -> Color:
        return Color(*self.rgba())

    def rgb(self) -> color:
        return (self.r, self.g, self.b)

    def rgba(self) -> color:
        return (self.r, self.g, self.b, self.a)

    def lerp(self, other: Color, t: float) -> Color:
        lerp = color_lerp(self.rgba(), other.rgba(), t)
        return Color(lerp)

    def __setattr__(self, name, value):
        super().__setattr__(name, int(value))
    
    def __repr__(self) -> str:
        return f'{self.rgba()}'


class TransitionColor(Object):
    def __init__(self, start: Color|str, end: Color|str, transition_time: str|float, start_time: str|float=0):
        super().__init__(transition_time, start_time)
        Object.elements.append(self)
        self.end = get_color(end)
        self.color = self.start = get_color(start)
        self.a = self.color.a

    def copy(self) -> TransitionColor:
        copy = TransitionColor(self.start, self.end, self.transition_time, self.start_time)
        copy.a = self.a
        return copy

    def update_alpha(self, alpha: int|float) -> None:
        self.a = alpha

    def update(self) -> None:
        if not super().update(): return
        self.color = self.start.lerp(self.end, self.t)
        self.color.a = int(self.color.a * self.a / 255)

    def rgb(self) -> None:
        return self.color.rgb()
    
    def rgba(self) -> None:
        return self.color.rgba()


Color.PRIMARY_BLUE = Color('#597988')
Color.SECONDARY_BLUE = Color('#172724')

Color.BLACK = Color('#000000')
Color.GRAY = Color('#7f7f7f')
Color.WHITE = Color('#ffffff')
Color.RED = Color('#ff0000')
Color.ORANGE = Color('#ff7f00')
Color.YELLOW = Color('#ffff00')
Color.LIMA = Color('#7fff00')
Color.GREEN = Color('#00ff00')
Color.TEAL = Color('#00ff7f')
Color.CYAN = Color('#00ffff')
Color.AZURE = Color('#007fff')
Color.BLUE = Color('#0000ff')
Color.PURPLE = Color('#7f00ff')
Color.MAGENTA = Color('#ff00ff')
Color.PINK = Color('#ff007f')

Color.LIGHTGRAY = Color('#bfbfbf')

Color.DARKGRAY = Color('#3f3f3f')
Color.DARKRED = Color('#3f0000')
Color.DARKORANGE = Color('#7f3f00')
Color.DARKYELLOW = Color('#7f7f00')
Color.DARKLIMA = Color('#3f7f00')
Color.DARKGREEN = Color('#007f00')
Color.DARKTEAL = Color('#007f3f')
Color.DARKCYAN = Color('#007f7f')
Color.DARKAZURE = Color('#003f7f')
Color.DARKBLUE = Color('#00007f')
Color.DARKPURPLE = Color('#3f007f')
Color.DARKMAGENTA = Color('#7f007f')
Color.DARKPINK = Color('#7f003f')