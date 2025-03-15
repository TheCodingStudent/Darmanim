from __future__ import annotations
import math
import pygame
import numpy as np
import pygame.gfxdraw
from Darmanim.window import Window
from Darmanim.color import get_color
from Darmanim.globals import get_value, LerpValue


class Grid:
    def __init__(
        self,
        minx: float=-5, maxx: float=5,
        miny: float=-5, maxy: float=5,
        x_padding: float=1, y_padding: float=1,
        x_interval: float=1, y_interval: float=1,
        x_color: any='darkred', y_color: any='darkblue'
    ):
        self.graph = None
        self.minx, self.maxx = minx, maxx
        self.miny, self.maxy = miny, maxy

        self.x_len = (maxx - minx + 2*x_padding)
        self.y_len = (maxy - miny + 2*y_padding)
        self.x_padding = x_padding
        self.y_padding = y_padding
        self.x_range = np.arange(minx/x_interval, maxx/x_interval + 1) * x_interval
        self.y_range = np.arange(miny/y_interval, maxy/y_interval + 1) * y_interval

        self.has_zero_in_x = (minx <= 0 and maxx >= 0)
        self.has_zero_in_y = (miny <= 0 and maxy >= 0)

        self.x_color = get_color(x_color)
        self.y_color = get_color(y_color)
    
    def attach(self, graph: Graph) -> Grid:
        self.graph = graph
        self.x_pixels = self.convert_x_to_pixel(self.x_range)
        self.y_pixels = self.convert_y_to_pixel(self.y_range)
        self.rect = pygame.Rect(0, 0, self.graph.width, self.graph.height).inflate(-self.x_pixels[0], -self.y_pixels[-1])
        return self
    
    def convert_x_to_pixel(self, x: float|np.array) -> float|np.array:
        return (x - self.x_range[0] + self.x_padding) * self.graph.width / self.x_len

    def convert_y_to_pixel(self, y: float|np.array) -> float|np.array:
        return (-y + self.y_range[-1] + self.y_padding) * self.graph.height / self.y_len

    def draw_x_lines(self) -> None:
        for x in self.x_pixels:
            pygame.draw.line(self.graph.surface, self.x_color.rgb(), (x, self.rect.top), (x, self.rect.bottom))
    
    def draw_y_lines(self) -> None:
        for y in self.y_pixels:
            pygame.draw.line(self.graph.surface, self.y_color.rgb(), (self.rect.left, y), (self.rect.right, y))

    def show(self) -> None:
        if self.x_color is not None: self.draw_x_lines()
        if self.y_color is not None: self.draw_y_lines()
        


class Axis:
    def __init__(
        self,
        mark_x_at_zero: bool=True,
        mark_y_at_zero: bool=True,
        x_axis_color: any='red',
        y_axis_color: any='blue'
    ):
        self.mark_x_at_zero = mark_x_at_zero
        self.mark_y_at_zero = mark_y_at_zero
        self.x_axis_color = get_color(x_axis_color)
        self.y_axis_color = get_color(y_axis_color)
    
    def attach(self, graph: Graph) -> Axis:
        self.graph = graph
        return self

    def draw_x_line(self) -> None:
        if self.mark_x_at_zero and self.graph.grid.has_zero_in_x: x = self.graph.grid.convert_x_to_pixel(0)
        else: x = self.graph.grid.convert_x_to_pixel(self.graph.grid.minx)
        top, bottom = self.graph.grid.rect.top, self.graph.grid.rect.bottom
        pygame.draw.line(self.graph.surface, self.x_axis_color.rgb(), (x, top), (x, bottom), width=3)
    
    def draw_y_line(self) -> None:
        if self.graph.grid.has_zero_in_y and self.mark_y_at_zero: y = self.graph.grid.convert_y_to_pixel(0)
        else: y = self.graph.grid.convert_y_to_pixel(self.graph.grid.miny)
        left, right = self.graph.grid.rect.left, self.graph.grid.rect.right
        pygame.draw.line(self.graph.surface, self.y_axis_color.rgb(), (left, y), (right, y), width=3)

    def show(self) -> None:
        if self.x_axis_color: self.draw_x_line()
        if self.y_axis_color: self.draw_y_line()
            

class Graph:
    def __init__(
        self, size: tuple[int, int],
        grid: Grid|None=None,
        axis: Axis|None=None,
        color: any=None,
        border: any='white',
        border_width: int=1
    ):
        self.screen = None
        self.surface = pygame.Surface(size)
        self.width, self.height = size

        self.grid = grid.attach(self) if grid else Grid().attach(self)
        self.axis = axis.attach(self) if axis else Axis().attach(self)

        self.color = color
        self.border = get_color(border)
        self.border_width = border_width

        self.functions = []
    
    def attach(self, window: Window, x: int|None=None, y: int|None=None) -> None:
        self.screen = window.screen
        if self.color is None: self.color = window.color
        if x is None: self.x = (self.screen.get_width() - self.width) / 2
        else: self.x = x
        if y is None: self.y = (self.screen.get_height() - self.height) / 2
        else: self.y = y

    def draw_border(self) -> None:
        if (self.border is None) or (self.border_width == 0): return
        pygame.draw.rect(self.surface, self.border.rgb(), (0, 0, self.width, self.height), width=self.border_width)

    def show(self) -> None:
        self.surface.fill(self.color.rgb())

        self.grid.show()
        self.axis.show()

        for function in self.functions:
            function.update()
            function.show()

        self.draw_border()
        self.screen.blit(self.surface, (self.x, self.y))
    
    def add(self, function: Function) -> None:
        self.functions.append(function)
        function.attach(self)
    
    def add_function(self, function: callable, call_update: bool=False) -> None:
        return self.add(Function(function, call_update))


class Function:
    def __init__(
        self, function: callable,
        call_update: bool=False,
        resolution: float=0.01,
        color: any='yellow',
        width: int=1,
        animation_time: any=None,
        antialiasing: bool=False,
        **kwargs
    ):
        self.function = function
        self.call_update = call_update
        self.resolution = get_value(resolution)
        self.color = get_color(color)
        self.width = get_value(width)

        if animation_time is None: self.animation_time = animation_time
        else: self.animation_time = LerpValue(0, 1, animation_time)
        self.antialiasing = antialiasing

        self.kwargs = kwargs
    
    def set_kwargs(self, **kwargs) -> None:
        self.kwargs |= kwargs

    def update(self, update_values: bool=False) -> None:
        if not (self.call_update or update_values): return
        resolution = self.resolution.get()
        self.x = np.arange(self.graph.grid.minx, self.graph.grid.maxx + resolution, resolution)
        self.y = self.function(self.x, **self.kwargs)

        if self.animation_time:
            i = int(self.animation_time.get() * len(self.x))
            self.y[i:] = 0

        self.x_pixels = self.graph.grid.convert_x_to_pixel(self.x)
        self.y_pixels = self.graph.grid.convert_y_to_pixel(self.y)
        self.coordinates = np.column_stack((self.x_pixels, self.y_pixels))

    def attach(self, graph: Graph) -> None:
        self.graph = graph
        self.update(update_values=True)
    
    def draw_antialiasing(self) -> None:
        width = self.width.get()
        for p0, p1 in zip(self.coordinates[:-1], self.coordinates[1:]):
            normal = p1 - p0
            magnitude = math.hypot(normal[0], normal[1])
            normal[0], normal[1] = normal[1], -normal[0]
            
            try: normal = width * normal / (2 * magnitude)
            except ZeroDivisionError: continue

            a = p0 + normal
            b = p0 - normal
            c = p1 - normal
            d = p1 + normal

            try: 
                pygame.gfxdraw.filled_polygon(self.graph.surface, (a, b, c, d), self.color.rgb())
                pygame.gfxdraw.aapolygon(self.graph.surface, (a, b, c, d), self.color.rgb())
            except ValueError: pass

    def show(self) -> None:
        if self.width.get() == 1:
            return pygame.draw.aalines(self.graph.surface, self.color.rgb(), False, self.coordinates)
        
        if self.antialiasing: return self.draw_antialiasing()
        pygame.draw.lines(self.graph.surface, self.color.rgb(), False, self.coordinates, width=self.width.get(int))


class AxisLabels:
    def __init__(self, graph: Graph):
        ...
    
    def show(self) -> None:
        ...