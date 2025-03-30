from __future__ import annotations
import math
from Darmanim.time import time
from Darmanim.values import Object


def get_color(value: any) -> Color:
    if value is None: return None
    if isinstance(value, str) and hasattr(Style, value): return getattr(Style, value)
    if isinstance(value, (Color, LerpColor, SwitchColor)): return value
    return Color(value)


def lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t


class Color:
    def __init__(self, value: any):
        self.a = 255

        if isinstance(value, (list, tuple)):
            if len(value) == 3: self.r, self.g, self.b = value
            if len(value) == 4: self.r, self.g, self.b, self.a = value
        elif isinstance(value, str):
            if value.startswith('#'):
                self.r = int(value[1:3], base=16)
                self.g = int(value[3:5], base=16)
                self.b = int(value[5:7], base=16)
                if len(value) == 9: self.a = int(value[7:9], base=16)
            else:
                color = getattr(Color, value.lower())
                self.r, self.g, self.b = color.rgb()
    
    def rgb(self) -> tuple[int, int, int]:
        return (int(self.r), int(self.g), int(self.b))

    def lerp(self, other: Color, t: float) -> Color:
        r = lerp(self.r, other.r, t)
        g = lerp(self.g, other.g, t)
        b = lerp(self.b, other.b, t)
        return Color((r, g, b))
    
    def slerp(self, other: Color, t: float) -> Color:
        r1, r2 = (self.r/255)**2, (other.r/255)**2
        g1, g2 = (self.g/255)**2, (other.g/255)**2
        b1, b2 = (self.b/255)**2, (other.b/255)**2

        r = 255 * math.sqrt(lerp(r1, r2, t))
        g = 255 * math.sqrt(lerp(g1, g2, t))
        b = 255 * math.sqrt(lerp(b1, b2, t))

        return Color((r, g, b))
    
    def __add__(self, other: Color) -> Color:
        r = self.r + other.r
        g = self.g + other.g
        b = self.b + other.b
        return Color((r, g, b))
    
    def __sub__(self, other: Color) -> Color:
        r = self.r - other.r
        g = self.g - other.g
        b = self.b - other.b
        return Color((r, g, b))

    def __mul__(self, other: float) -> Color:
        r = self.r * other
        g = self.g * other
        b = self.b * other
        return Color((r, g, b))

    def __repr__(self) -> str:
        return f'{self.rgb()=}'


class SwitchColor(Object):
    def __init__(self, start: any, end: any, switch_time: time):
        super().__init__()
        self.start = get_color(start)
        self.end = get_color(end)
        self.switch_time = switch_time
    
    def update(self) -> None:
        self.color = self.start if self.time < self.switch_time else self.end

    def rgb(self) -> tuple[int, int, int]:
        return self.color.rgb()


class LerpColor(Object):
    def __init__(self, start: any, end: any, transition_time: time, start_time: time=0):
        super().__init__(start_time)
        self.color = self.start = get_color(start)
        self.end = get_color(end)

        self.start_time = start_time
        self.transition_time = transition_time
    
    def update(self) -> bool:
        t = min(self.time/self.transition_time, 1)
        self.color = self.start + (self.end - self.start) * t

        return t == 1
    
    def rgb(self) -> tuple[int, int, int]:
        return self.color.rgb()


Color.white     = Color('#ffffff')
Color.lightgray = Color('#bfbfbf')
Color.gray      = Color('#7f7f7f')
Color.darkgray  = Color('#3f3f3f')
Color.black     = Color('#000000')

Color.greensage   = Color('#92946f')
Color.greenforest = Color('#6b8c53')
Color.babypink    = Color('#e3b0b0')

Color.red       = Color('#ff0000')
Color.orange    = Color('#ff7f00')
Color.yellow    = Color('#ffff00')
Color.lime      = Color('#7fff00')
Color.green     = Color('#00ff00')
Color.teal      = Color('#00ff7f')
Color.cyan      = Color('#00ffff')
Color.azure     = Color('#007fff')
Color.blue      = Color('#0000ff')
Color.purple    = Color('#7f00ff')
Color.magenta   = Color('#ff00ff')
Color.pink      = Color('#ff007f')
Color.brown     = Color('#754930')

Color.darkred       = Color('#7f0000')
Color.darkorange    = Color('#7f3f00')
Color.darkyellow    = Color('#7f7f00')
Color.darklime      = Color('#3f7f00')
Color.darkgreen     = Color('#007f00')
Color.darkteal      = Color('#007f3f')
Color.darkcyan      = Color('#007f7f')
Color.darkazure     = Color('#003f7f')
Color.darkblue      = Color('#00007f')
Color.darkpurple    = Color('#3f007f')
Color.darkmagenta   = Color('#7f007f')
Color.darkpink      = Color('#7f003f')
Color.darkbrown     = Color('#27160e')

Color.pastelred    = Color('#ff779c')
Color.pastelorange = Color('#faa39d')
Color.pastelyellow = Color('#fbf8cc')
Color.pastelgreen  = Color('#b9fbc0')
Color.pastelaqua   = Color('#98f5e1')
Color.pastelcyan   = Color('#8eecf5')
Color.pastelazure  = Color('#90dbf4')
Color.pastelblue   = Color('#a3c4f3')
Color.pastelpurple = Color('#cfbaf0')
Color.pastelviolet = Color('#f1c0e8')
Color.pastelpink   = Color('#ffcfd2')

Color.lightred      = Color('#ff7f7f')
Color.lightorange   = Color('#ffbf3f')
Color.lightyellow   = Color('#ffff7f')
Color.lightlime     = Color('#bfff7f')
Color.lightgreen    = Color('#00ff7f')
Color.lightteal     = Color('#7fffbf')
Color.lightcyan     = Color('#7fffff')
Color.lightazure    = Color('#7fbfff')
Color.lightblue     = Color('#7f7fff')
Color.lightpurple   = Color('#bf7fff')
Color.lightmagenta  = Color('#ff7fff')
Color.lightpink     = Color('#ff7fbf')
Color.lightbrown    = Color('#ceaf93')


class Style:
    background = Color('#272d47')
    x_grid_line = Color('#99a0ba')
    y_grid_line = Color('#99a0ba')
    x_axis_line = Color('#ccd4eb')
    y_axis_line = Color('#ccd4eb')
    border  = Color.white
    red     = Color('#ef346b')
    orange  = Color('#dc8c69')
    yellow  = Color('#fec01f')
    green   = Color('#3cd68d') 
    cyan    = Color('#38cbc9') 
    blue    = Color('#34c1f7')
    purple  = Color('#9b62d3') 
    violet  = Color('#dc67cf')
    white   = Color('#f7f7f7')
    black   = Color('#171d37')
    