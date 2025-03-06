from __future__ import annotations
import pygame
import numpy as np

from Darmanim.globals import Object, parse_size, iterable, parse_base, parse_time_to_sec, Event
from Darmanim.color import Color, TransitionColor, get_color

class AxisLabels:
    letters: str='abcdefghijklmnopqrstuvwxyz'
    def __init__(
        self, axis: str,
        font: str='Cambria Math', font_size: int=18,
        values: list[str]|None=None,
        color: Color=Color.LIGHTGRAY,
        bold: bool=True, 
        decimals: int=3
    ):
        self.axis = axis
        self.bold = bold
        self.color = get_color(color)
        self.values = values
        self.font_type = font
        self.decimals = decimals
        self.font_size = font_size
        self.labels = []

    def attach(self, graph: Graph) -> AxisLabels:
        self.graph = graph

        self.base = getattr(graph.grid, f'{self.axis}_base')
        axis_values = getattr(graph.grid, f'{self.axis}_axis')
        if self.base != ('', 1):
            axis_values = [parse_base(value, self.base, self.decimals) for value in axis_values]
        else: axis_values = np.round(axis_values, self.decimals)

        axis_length = len(axis_values)

        self.font_size = parse_size(self.font_size, self.graph.margin/2, cast=int)
        self.font = pygame.font.SysFont(self.font_type, self.font_size, bold=self.bold)
        self.values = self.values if self.values is not None and any(self.values) else axis_values
        self.values = self.values[:axis_length]
        self.labels = self.update_labels()
        self.label_rects = self.draw_x_axis() if self.axis=='x' else self.draw_y_axis()

        return self

    def update_labels(self) -> list[pygame.Surface]:
        return [self.font.render(str(value), True, self.color.rgb()) for value in self.values]

    def draw_x_axis(self) -> list[pygame.Rect]:
        result = []
        for i, label in enumerate(self.labels):
            rect = label.get_rect(center=(self.graph.grid.x[i] + self.graph.margin, self.graph.height - self.graph.margin/2))
            result.append(rect)
        
        return result

    def draw_y_axis(self) -> list[pygame.Rect]:
        result = []
        for i, label in enumerate(self.labels):
            rect = label.get_rect(center=(self.graph.margin/2, self.graph.grid.y[i] + self.graph.margin))
            result.append(rect)
        
        return result
    
    def update(self) -> None:
        if not isinstance(self.color, TransitionColor): return
        self.labels = self.update_labels()

    def draw(self) -> None:
        if self.graph is None: return
        self.update()
        
        for label, rect in zip(self.labels, self.label_rects):
            self.graph.blit(label, rect)


class Space(pygame.Surface):
    def __init__(
        self,
        minx: float=-5, maxx: float=5,
        miny: float=-5, maxy: float=5,
        padding: float=0.5,
        x_base: tuple[str, int]=('', 1),
        y_base: tuple[str, int]=('', 1),
    ):
        self.padding = padding
        self.x_base = x_base
        self.y_base = y_base
        self.miny, self.maxy = miny * y_base[1], maxy * y_base[1]
        self.minx, self.maxx = minx * x_base[1], maxx * x_base[1]
        self.x_width = self.maxx - self.minx
        self.y_height = self.maxy - self.miny


class Grid(Space):
    def __init__(
        self,
        padding: float=0.5,
        minx: float=-5, maxx: float=5,
        miny: float=-5, maxy: float=5,
        x_interval: float=1,
        y_interval: float=1,
        x_secondary: float=0.5,
        y_secondary: float=0.5,
        x_base: tuple[str, int]=('', 1),
        y_base: tuple[str, int]=('', 1),
        x_color: tuple[Color, Color]|Color=(Color.PRIMARY_BLUE, Color.SECONDARY_BLUE),
        y_color: tuple[Color, Color]|Color=(Color.PRIMARY_BLUE, Color.SECONDARY_BLUE)

    ):
        super().__init__(minx, maxx, miny, maxy, padding, x_base, y_base)
        self.zero_in_x_axis = (minx < 0 and maxx >= 0) or (minx <= 0 and maxx > 0)
        self.zero_in_y_axis = (miny < 0 and maxy >= 0) or (miny <= 0 and maxy > 0)
        self.x_axis = self.get_axis('x', x_interval * x_base[1])
        self.y_axis = self.get_axis('y', y_interval * y_base[1])
        self.x_secondary = self.get_axis('x', x_secondary * x_base[1])
        self.y_secondary = self.get_axis('y', y_secondary * y_base[1])
        self.x_color = x_color if isinstance(x_color, iterable) else (x_color, x_color)
        self.y_color = y_color if isinstance(y_color, iterable) else (y_color, y_color)
    
    def get_axis(self, axis: str, interval: float) -> np.array:
        min_value = getattr(self, f'min{axis}')
        max_value = getattr(self, f'max{axis}')
        has_zero = getattr(self, f'zero_in_{axis}_axis')

        if not has_zero:
            return np.arange(min_value, max_value + interval, interval)

        if min_value % interval:
            min_axis = np.arange(interval, -min_value, interval)
            min_axis = -np.append(min_axis, -min_value)[::-1]
        else: min_axis = np.arange(min_value, 0, interval)

        max_axis = np.append(np.arange(0, max_value, interval), max_value)
        return np.concatenate((min_axis, max_axis))

    def get_grid_axis(self, values: np.array, axis: str) -> np.array:
        min_value = getattr(self, f'min{axis}')
        margin = self.graph.margin
        if axis == 'x':
            return (values - min_value + self.padding) * self.width

        return self.graph.height - 2*margin - (values - min_value + self.padding) * self.height

    def attach(self, graph: Graph) -> Grid:
        self.graph = graph
        margin = self.graph.margin
        width = self.graph.width
        height = self.graph.height

        self.width = (width - 2*margin) / (self.maxx - self.minx + 1)
        self.height = (height - 2*margin) / (self.maxy - self.miny + 1)

        self.x = self.get_grid_axis(self.x_axis, 'x')
        self.y = self.get_grid_axis(self.y_axis, 'y')
        self.xs = self.get_grid_axis(self.x_secondary, 'x')
        self.ys = self.get_grid_axis(self.y_secondary, 'y')

        self.rect = pygame.Rect(0, 0, width-2*margin, height-2*margin)

        return self
    
    def draw_vertical(self, x: float, index: int=0) -> None:
        color = self.x_color[index].rgb()
        pygame.draw.line(self.graph.inner, color, (x, self.rect.top), (x, self.rect.bottom))
    
    def draw_horizontal(self, y: float, index: int=0) -> None:
        color = self.y_color[index].rgb()
        pygame.draw.line(self.graph.inner, color, (self.rect.left, y), (self.rect.right, y))

    def draw(self) -> None:
        for xs in self.xs: self.draw_vertical(xs, index=1)
        for ys in self.ys: self.draw_horizontal(ys, index=1)
        for x in self.x: self.draw_vertical(x)
        for y in self.y: self.draw_horizontal(y)


class Axis:
    def __init__(
        self,
        mark_at_zero: bool=True,
        width: int=3,
        x_color: Color=Color.AZURE,
        y_color: Color=Color.RED
    ):
        self.width = width
        self.x_color = x_color
        self.y_color = y_color
        self.mark_at_zero = mark_at_zero
    
    def attach(self, graph: Graph) -> Axis:
        self.graph = graph

        if self.graph.grid.zero_in_x_axis:
            self.x_zero = self.graph.grid.x[self.graph.grid.x_axis == 0][0]

        if self.graph.grid.zero_in_y_axis:
            self.y_zero = self.graph.grid.y[self.graph.grid.y_axis == 0][0]

        margin = self.graph.margin
        padding = self.graph.grid.padding

        if self.mark_at_zero:
            self.x = self.x_zero if self.graph.grid.zero_in_x_axis else -1
            self.y = self.y_zero if self.graph.grid.zero_in_y_axis else -1
        else:
            self.x = margin + padding*self.graph.grid.width
            self.y = self.graph.height - (margin + padding*self.graph.grid.height)

        self.vertical = ((self.x, 0), (self.x, self.graph.height))
        self.horizontal = ((0, self.y), (self.graph.width, self.y))

        return self

    def draw(self) -> None:
        pygame.draw.line(self.graph.inner, self.x_color.rgb(), *self.vertical, width=self.width)
        pygame.draw.line(self.graph.inner, self.y_color.rgb(), *self.horizontal, width=self.width)


class Graph(pygame.Surface):
    def __init__(
        self, window: pygame.Surface|None=None,
        size: tuple[int, int]=(0, 0),
        x: int|None=None, y: int|None=None,
        margin: int=50,
        axis: Axis|None=None,
        grid: Grid|None=None,
        x_labels: AxisLabels|None=None,
        y_labels: AxisLabels|None=None,
        border: int=0,
        fill: Color|str=''
    ):

        self.attached = False
        self.width, self.height = size
        self.background = get_color(fill)

        self.functions = []
        self.border = border
        self.margin = margin
        self.x, self.y = x, y

        self.grid = grid or Grid()
        self.axis = axis or Axis()
        self.x_labels = x_labels or AxisLabels(axis='x')
        self.y_labels = y_labels or AxisLabels(axis='y')

        if window is not None: self.attach(window)

    def attach(self, window: pygame.Surface) -> None:
        self.attached = True

        Object.elements.append(self)
        self.surface = window.surface
        if self.width==0: self.width = window.width
        if self.height==0: self.height = window.height
        pygame.Surface.__init__(self, (self.width, self.height))

        self.inner = pygame.Surface((self.width-2*self.margin, self.height-2*self.margin), pygame.SRCALPHA)
        self.inner.convert_alpha()

        if not self.background: self.background = window.fill

        if self.x is None: self.x = (window.width-self.width) / 2
        if self.y is None: self.y = (window.height-self.height) / 2
        self.rect = self.get_rect(topleft=(self.x, self.y))

        self.grid = self.grid.attach(self)
        self.axis = self.axis.attach(self)
        self.x_labels = self.x_labels.attach(self)
        self.y_labels = self.y_labels.attach(self)

        for function in self.functions: function.attach(self)

    def draw(self) -> None:
        self.fill(self.background.rgba())
        self.inner.fill(self.background.rgba())

        self.grid.draw()
        self.axis.draw()
        self.x_labels.draw()
        self.y_labels.draw()

        for function in self.functions: function.draw()

        if self.border == 0: return
        pygame.draw.rect(self, 'white', (0, 0, *self.get_size()), width=self.border)

    def update(self) -> None:
        self.draw()
        self.blit(self.inner, (self.margin, self.margin))
        self.surface.blit(self, self.rect.topleft)

    def attach_function(self, function: Function) -> None:
        self.functions.append(function.attach(self))

    def add(self, function: Function|callable[(float, ), float], time: str|float=0) -> None:
        if callable(function): function = Function(function)

        time = parse_time_to_sec(time)
        if self.attached: function = function.attach(self)

        if not time: return self.functions.append(function)

        if isinstance(function.color, TransitionColor) and function.color.start_time == 0:
            function.color.start_time = time
        return Event(function=self.attach_function, args=(function, ), event_time=time)
    
    def remove(self, function: Function, time: str|int=0, **kwargs) -> None:
        if time: return Event(function=self.functions.remove, args=(function, ), event_time=time)
        return self.functions.remove(function)


class Function(Object):
    def __init__(
        self,
        function: callable[(float, ), float],
        color: Color|str='yellow', resolution: float=0.01,
        width: int=3, call_update: bool=False,
        fill: Color|str|None=None
    ):
        super().__init__()

        self.color = get_color(color)
        self.fill = get_color(fill)
        self.closed = self.fill is not None

        self.width = width
        self.function = function
        self.resolution = resolution

        self.call_update = call_update

    def get_y_values(self) -> np.array:
        try:
            return self.function(self.x_axis.copy())
        except TypeError:
            return np.array([self.function(x) for x in self.x_axis])

    def update(self) -> None:
        y_axis = self.get_y_values()
        self.segments = self.find_segments(y_axis)
        self.y = self.graph.grid.get_grid_axis(y_axis, 'y')
        self.coordinates = np.stack((self.x, self.y), axis=1)

    def find_segments(self, values: np.array) -> list[list[tuple, tuple]]:
        segments = []

        current_segment = []
        bool_values = (values < -self.infinity) + (values > self.infinity) + np.isnan(values)

        for i, value in enumerate(1 - bool_values):
            if (value == True) and not current_segment and i > 0:
                current_segment.append(i - 1)
            elif (value == False) and current_segment:

                if abs(current_segment[0] - i + 1) > 1:
                    current_segment.append(i)
                    segments.append(current_segment)
                current_segment = []

        if current_segment:
            current_segment.append(len(values))
            segments.append(current_segment)

        if not segments: segments.append((0, len(values)))

        return segments


    def attach(self, graph: Graph) -> Function:
        self.graph = graph
        self.infinity = 2 * max(abs(self.graph.grid.miny), abs(self.graph.grid.maxy))
        self.x_axis = self.graph.grid.get_axis('x', self.resolution)
        self.x = self.graph.grid.get_grid_axis(self.x_axis, 'x')
        self.update()

        return self
    
    def draw(self) -> None:
        if self.call_update: self.update()
        for start, end in self.segments:
            if self.closed: pygame.draw.polygon(self.graph.inner, self.fill.rgba(), self.coordinates[start:end])
            pygame.draw.lines(self.graph.inner, self.color.rgba(), False, self.coordinates[start:end], width=self.width)