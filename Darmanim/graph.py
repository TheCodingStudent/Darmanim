from __future__ import annotations
import math
import pygame
import numpy as np
import pygame.gfxdraw
from Darmanim.time import Clock
from Darmanim.window import Window
from Darmanim.color import get_color
from Darmanim.globals import get_value, LerpValue

type unit = float
type pixel = float


class Grid:
    def __init__(
        self,
        minx: unit=-5, maxx: unit=5,
        miny: unit=-5, maxy: unit=5,
        x_padding: unit=1, y_padding: unit=1,
        x_interval: unit=1, y_interval: unit=1,
        x_stroke: pixel=1, y_stroke: pixel=1,
        x_color: any='x_grid_line', y_color: any='y_grid_line'
    ):
        self.graph = None
        self.minx, self.maxx = minx, maxx
        self.miny, self.maxy = miny, maxy

        self.x_len = (maxx - minx + 2*x_padding)
        self.y_len = (maxy - miny + 2*y_padding)
        self.x_padding = x_padding
        self.y_padding = y_padding
        self.x_interval = x_interval
        self.y_interval = y_interval
        self.x_color = get_color(x_color)
        self.y_color = get_color(y_color)
        self.x_stroke = x_stroke
        self.y_stroke = y_stroke

        self.center = [0, 0]

    def square(
        size: unit,
        x_padding: unit=1, y_padding: unit=1,
        x_interval: unit=1, y_interval: unit=1,
        x_stroke: pixel=1, y_stroke: pixel=1,
        x_color: any='x_grid_line', y_color: any='y_grid_line'
    ) -> Grid:
        return Grid(
            -size, size, -size, size,
            x_padding, y_padding, x_interval, y_interval,
            x_stroke, y_stroke, x_color, y_color
        )

    def attach(self, graph: Graph) -> Grid:
        self.graph = graph
        self.update()
        return self
    
    def center_at(self, x: unit, y: unit) -> None:
        dx = x - self.center[0]
        dy = y - self.center[1]
        self.shift(dx, dy)
        self.update()

    def shift(self, dx: unit, dy: unit) -> None:
        self.minx += dx
        self.maxx += dx
        self.miny += dy
        self.maxy += dy

        self.center[0] += dx
        self.center[1] += dy

    def update(self) -> None:
        minx, maxx = (self.minx - self.x_padding) / self.x_interval, (self.maxx + self.x_padding) / self.x_interval
        miny, maxy = (self.miny - self.y_padding) / self.y_interval, (self.maxy + self.y_padding) / self.y_interval

        self.x_range = np.arange(minx + self.x_interval, maxx + self.x_interval) // 1 * self.x_interval
        self.y_range = np.arange(miny + self.y_interval, maxy + self.y_interval) // 1 * self.y_interval

        self.has_zero_in_x = (minx <= 0 and maxx >= 0)
        self.has_zero_in_y = (miny <= 0 and maxy >= 0)

        self.x_pixels = self.convert_x_to_pixel(self.x_range)
        self.y_pixels = self.convert_y_to_pixel(self.y_range)

        self.width = np.max(self.x_pixels) - np.min(self.x_pixels)
        self.height = np.max(self.y_pixels) - np.min(self.y_pixels)

        dx = self.convert_dx_to_pixel(self.x_padding)
        dy = -self.convert_dy_to_pixel(self.y_padding)
        self.rect = pygame.Rect(0, 0, self.graph.width, self.graph.height).inflate(-dx, -dy)

    def convert_x_to_pixel(self, x: unit|np.array) -> pixel|np.array:
        return (x - self.minx + self.x_padding) * self.graph.width / self.x_len

    def convert_dx_to_pixel(self, dx: unit|np.array) -> pixel|np.array:
        return self.convert_x_to_pixel(dx) - self.convert_x_to_pixel(0)

    def convert_y_to_pixel(self, y: unit|np.array) -> pixel|np.array:
        return (-y - self.miny + self.y_padding) * self.graph.height / self.y_len

    def convert_dy_to_pixel(self, dy: unit|np.array) -> pixel|np.array:
        return self.convert_y_to_pixel(dy) - self.convert_y_to_pixel(0)

    def draw_x_lines(self) -> None:
        for x in self.x_pixels:
            if x < self.rect.left or x > self.rect.right: continue
            pygame.draw.line(self.graph.surface, self.x_color.rgb(), (x, self.rect.top), (x, self.rect.bottom), self.x_stroke)

    def draw_y_lines(self) -> None:
        y_padding = self.convert_dy_to_pixel(self.y_padding)
        for y in self.y_pixels:
            y = y % (self.rect.height - y_padding)
            if y > self.rect.bottom or y < self.rect.top: continue
            pygame.draw.line(self.graph.surface, self.y_color.rgb(), (self.rect.left, y), (self.rect.right, y), self.y_stroke)

    def show(self) -> None:
        if self.x_color is not None: self.draw_x_lines()
        if self.y_color is not None: self.draw_y_lines()


class BlankGrid(Grid):
    def __init__(
        self,
        minx: unit=-5, maxx: unit=5,
        miny: unit=-5, maxy: unit=5,
        x_padding: unit=1, y_padding: unit=1,
        x_interval: unit=1, y_interval: unit=1
    ):
        super().__init__(minx, maxx, miny, maxy, x_padding, y_padding, x_interval, y_interval, 1, 1, None, None)

    def square(
        size: unit,
        x_padding: unit=1, y_padding: unit=1,
        x_interval: unit=1, y_interval: unit=1
    ) -> BlankGrid:
        return BlankGrid(
            -size, size, -size, size,
            x_padding, y_padding, x_interval, y_interval
        )


class Arrow:
    def __init__(
        self,
        center: tuple[unit, unit]|Point,
        direction: tuple[unit, unit]|Point,
        width: pixel, height: pixel, 
        color: any='white',
        fill: any=None,
        stroke: pixel=0,
        static: bool=False
    ):
        if isinstance(center, Point): self.x, self.y = center.x, center.y
        else: self.x, self.y = get_value(center[0]), get_value(center[1])
        if isinstance(direction, Point): self.dx, self.dy = direction.x, direction.y
        else: self.dx, self.dy = get_value(direction[0]), get_value(direction[1])

        self.static = static

        self.width = get_value(width)
        self.height = get_value(height)
        self.color = get_color(color)
        self.fill = get_color(fill)
        self.stroke = get_value(stroke)
    
    def attach(self, graph: Graph) -> Arrow:
        self.graph = graph

    def show(self) -> None:
        x, y = self.x.get(), self.y.get()
        dx, dy = self.dx.get(), -self.dy.get()

        x = self.x if self.static else self.graph.grid.convert_x_to_pixel(x)
        y = self.y if self.static else self.graph.grid.convert_y_to_pixel(y)

        center = pygame.Vector2(x, y)
        direction = pygame.Vector2(dx, dy).normalize()
        width, height = self.width.get(), self.height.get()
        a = center + direction * height
        b = center + direction.rotate(90) * width/2
        c = center - direction.rotate(90) * width/2

        if self.fill is not None: pygame.draw.polygon(self.graph.surface, self.fill.rgb(), (a, b, c))
        pygame.draw.polygon(self.graph.surface, self.color.rgb(), (a, b, c), self.stroke)


class Axis:
    def __init__(
        self,
        mark_x_at_zero: bool=True,
        mark_y_at_zero: bool=True,
        draw_x_axis_arrow: bool=True,
        draw_y_axis_arrow: bool=True,
        x_axis_color: any='x_axis_line',
        y_axis_color: any='y_axis_line',
        x_axis_stroke: pixel=3,
        y_axis_stroke: pixel=3
    ):
        self.mark_x_at_zero = mark_x_at_zero
        self.mark_y_at_zero = mark_y_at_zero
        self.draw_x_axis_arrow = draw_x_axis_arrow
        self.draw_y_axis_arrow = draw_y_axis_arrow
        self.x_axis_color = get_color(x_axis_color)
        self.y_axis_color = get_color(y_axis_color)
        self.x_axis_stroke = get_value(x_axis_stroke)
        self.y_axis_stroke = get_value(y_axis_stroke)
    
    def attach(self, graph: Graph) -> Axis:
        self.graph = graph
        return self

    def draw_y_line(self) -> None:
        if self.mark_x_at_zero: 
            if self.graph.grid.has_zero_in_x: x = self.graph.grid.convert_x_to_pixel(0)
            else: return
        else: x = self.graph.grid.convert_x_to_pixel(self.graph.grid.minx)
        top, bottom = self.graph.grid.rect.top, self.graph.grid.rect.bottom
        pygame.draw.line(self.graph.surface, self.y_axis_color.rgb(), (x, top), (x, bottom), self.y_axis_stroke)
    
    def draw_x_line(self) -> None:
        if self.graph.grid.has_zero_in_y:
            if self.mark_y_at_zero: y = self.graph.grid.convert_y_to_pixel(0)
            else: return
        else: y = self.graph.grid.convert_y_to_pixel(self.graph.grid.miny)
        left, right = self.graph.grid.rect.left, self.graph.grid.rect.right
        pygame.draw.line(self.graph.surface, self.x_axis_color.rgb(), (left, y), (right, y), self.x_axis_stroke)

    def show(self) -> None:
        if self.x_axis_color: self.draw_x_line()
        if self.y_axis_color: self.draw_y_line()


class Graph:
    def __init__(
        self, size: tuple[pixel, pixel],
        grid: Grid|None=None,
        axis: Axis|None=None,
        color: any=None,
        border: any='white',
        border_width: pixel=1
    ):
        self.screen = None
        self.surface = pygame.Surface(size)
        self.width, self.height = size

        self.grid = grid.attach(self) if grid else Grid().attach(self)
        self.axis = axis.attach(self) if axis else Axis().attach(self)

        self.color = color
        self.border = get_color(border)
        self.border_width = border_width

        self.dx = self.dy = None
        self.call_update = False

        self.elements = []
    
    def attach(self, window: Window, x: pixel|None=None, y: pixel|None=None) -> None:
        self.screen = window.screen
        if self.color is None: self.color = window.color
        if x is None: self.x = (self.screen.get_width() - self.width) / 2
        else: self.x = x
        if y is None: self.y = (self.screen.get_height() - self.height) / 2
        else: self.y = y

    def draw_border(self) -> None:
        if (self.border is None) or (self.border_width == 0): return
        pygame.draw.rect(self.surface, self.border.rgb(), (0, 0, self.width, self.height), width=self.border_width)

    def update(self) -> None:
        if not self.call_update: return
        for element in self.elements:
            if isinstance(element, Function): element.update(True)

        if self.dx is None and self.dy is None: return
        self.grid.center_at(self.dx.get(), self.dy.get())

    def shift(self, dx: unit, dy: unit, transition_time: float=0, start_time: float=0) -> None:
        self.call_update = True
        dy = -dy
        if transition_time == 0: self.dx, self.dy = get_value(dx), get_value(dy)
        else:
            if self.dx is None: self.dx = 0
            if self.dy is None: self.dy = 0
            self.dx = LerpValue(self.dx, dx, transition_time, start_time)
            self.dy = LerpValue(self.dy, dy, transition_time, start_time)

    def show(self) -> None:
        self.surface.fill(self.color.rgb())

        self.grid.show()
        self.axis.show()

        for element in self.elements:
            if hasattr(element, 'update'): element.update()
            element.show()

        self.draw_border()
        self.screen.blit(self.surface, (self.x, self.y))
    
    def add(self, *elements: any) -> any:
        for element in elements:
            element.attach(self)
            self.elements.append(element)
        
        if len(elements) == 1: return elements[0]
        return elements


class BlankGraph(Graph):
    def __init__(
        self, size: tuple[pixel, pixel],
        grid: Grid|None=None,
        color: any=None,
        border: any='white',
        border_width: pixel=1
    ):
        grid = BlankGrid() if grid is None else grid
        super().__init__(size, grid, None, color, border, border_width)
    
    def show(self) -> None:
        self.surface.fill(self.color.rgb())

        self.grid.show()

        for element in self.elements:
            if hasattr(element, 'update'): element.update()
            element.show()

        self.draw_border()
        self.screen.blit(self.surface, (self.x, self.y))


class Function:
    def __init__(
        self, function: callable,
        resolution: unit=0.01,
        color: any='yellow',
        stroke: pixel=1,
        minx: unit|None=None, maxx: unit|None=None,
        animation_time: any=None,
        antialiasing: bool=False,
        call_update: bool=False,
        **kwargs
    ):
        self.function = function
        self.call_update = call_update
        self.resolution = get_value(resolution)
        self.color = get_color(color)
        self.stroke = get_value(stroke)

        self.minx, self.maxx = minx, maxx

        if animation_time is None: self.animation_time = animation_time
        else: self.animation_time = LerpValue(0, 1, animation_time)
        self.antialiasing = antialiasing

        self.kwargs = kwargs
    
    def point_along(
        self, minx: unit=None, maxx: unit=None,
        radius: pixel = 10, stroke: pixel = 3,
        color: any = 'white', fill: any = 'black',
        transition_time: float=1
    ) -> Point:
        minx = minx if minx is not None else self.minx if self.minx is not None else self.graph.grid.minx
        maxx = maxx if maxx is not None else self.maxx if self.minx is not None else self.graph.grid.maxx

        x = LerpValue(minx, maxx, transition_time)
        y = LerpValue(minx, maxx, transition_time, function=self.function)
        point = Point(x, y, radius, stroke, color, fill)
        point.graph = self.graph
        return point

    def set_kwargs(self, **kwargs) -> None:
        self.kwargs |= kwargs

    def update(self, update_values: bool=False) -> None:
        if not (self.call_update or update_values): return
        resolution = self.resolution.get()
        minx = (self.minx or self.graph.grid.minx) - self.graph.grid.x_padding/2
        maxx = (self.maxx or self.graph.grid.maxx) + self.graph.grid.x_padding/2

        self.x = np.arange(minx, maxx, resolution)
        self.y = self.function(self.x, **self.kwargs)

        if self.animation_time:
            i = int(self.animation_time * len(self.x))
            self.y[i:] = 0

        self.x_pixels = self.graph.grid.convert_x_to_pixel(self.x)
        self.y_pixels = self.graph.grid.convert_y_to_pixel(self.y)
        self.coordinates = np.column_stack((self.x_pixels, self.y_pixels))

    def attach(self, graph: Graph) -> None:
        self.graph = graph
        self.update(update_values=True)
    
    def draw_antialiasing(self) -> None:
        stroke = self.stroke.get()
        for p0, p1 in zip(self.coordinates[:-1], self.coordinates[1:]):
            normal = p1 - p0
            magnitude = math.hypot(normal[0], normal[1])
            normal[0], normal[1] = normal[1], -normal[0]
            
            try: normal = stroke * normal / (2 * magnitude)
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
        if self.stroke.get() == 1:
            return pygame.draw.aalines(self.graph.surface, self.color.rgb(), False, self.coordinates)
        
        if self.antialiasing: return self.draw_antialiasing()
        pygame.draw.lines(self.graph.surface, self.color.rgb(), False, self.coordinates, width=self.stroke.get(int))


class AxisLabels:
    def __init__(self, graph: Graph):
        ...
    
    def show(self) -> None:
        ...


class Path:
    def __init__(
        self, point: Point,
        color: any='white',
        fill: any=None,
        stroke: pixel=1,
        start_time: float=0,
        plot_time: float=float('inf')
    ):
        self.x, self.y = point.x, point.y
        self.color = get_color(color)
        self.fill = get_color(fill)
        self.stroke = get_value(stroke)

        self.start_time = start_time
        self.plot_time = plot_time
        self.x_points = np.array([])
        self.y_points = np.array([])

        self.path = []

    def update(self) -> None:
        time = Clock.time - self.start_time

        if time >= self.plot_time or time < 0: return
        self.x_points = np.append(self.x_points, self.x.get())
        self.y_points = np.append(self.y_points, self.y.get())

        x = self.graph.grid.convert_x_to_pixel(self.x_points)
        y = self.graph.grid.convert_y_to_pixel(self.y_points)
        self.path = np.column_stack((x, y))

    
    def attach(self, graph: Graph) -> Path:
        self.graph = graph
        return self

    def show(self) -> None:
        if len(self.path) < 2: return
        if self.fill is not None:
            pygame.draw.polygon(self.graph.surface, self.fill.rgb(), self.path)
        
        if self.stroke == 1:
            pygame.draw.aalines(self.graph.surface, self.color.rgb(), False, self.path)
        else:
            pygame.draw.lines(self.graph.surface, self.color.rgb(), False, self.path, self.stroke.get(int))


class Point:
    def __init__(self, x: unit, y: unit, radius: pixel=10, stroke: pixel=3, color: any='white', fill: any=None):
        self.x = get_value(x)
        self.y = get_value(y)
        self.stroke = get_value(stroke)
        self.radius = get_value(radius)

        self.color = get_color(color)
        self.fill = get_color(fill)
    
    def vertical_to(self, y: unit, color: any='white', stroke: pixel=1) -> Line:
        other = Point(self.x, y)
        return Line(self, other, color, stroke)

    def horizontal_to(self, x: unit|Point, color: any='white', stroke: pixel=1) -> Line:
        if isinstance(x, Point):
            other = Point(x.x, self.y)
            other.graph = x.graph
        else: other = Point(x, self.y)

        return Line(self, other, color, stroke)

    def line_to_point(self, other: Point, color: any='white', stroke: pixel=1) -> Line:
        return Line(self, other, color, stroke)

    def distance_to(self, other: Point) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)

    def from_list(points: list[tuple[unit, unit]], radius: pixel=10, stroke: pixel=3, color: any='white', fill: any='black') -> list[Point]:
        result = []
        for point in points:
            result.append(Point(*point, radius, stroke, color, fill))
        return result

    def attach(self, graph: Graph) -> Point:
        self.graph = graph
        return self

    def show(self) -> None:
        x = self.graph.grid.convert_x_to_pixel(self.x.get())
        y = self.graph.grid.convert_y_to_pixel(self.y.get())
        if self.fill: pygame.draw.circle(self.graph.surface, self.fill.rgb(), (x, y), self.radius)
        pygame.draw.circle(self.graph.surface, self.color.rgb(), (x, y), self.radius, width=self.stroke)
    
    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'


class Line:
    def __init__(
        self,
        start: tuple[unit, unit]|Point, end: tuple[unit, unit]|Point,
        color: any='white', stroke: pixel=1,
        transition_time: float=0, start_time: float=0
    ):
        self.start = start
        self.end = end
        self.color = get_color(color)
        self.stroke = get_value(stroke)
        self.transition_time = transition_time
        self.start_time = start_time

        self.cross_surface = False
        if isinstance(start, Point) and isinstance(end, Point):
            if hasattr(start, 'graph') and hasattr(end, 'graph'):
                self.cross_surface = start.graph != end.graph

    def point_along(
        self,
        radius: pixel = 10, stroke: pixel = 3,
        color: any = 'white', fill: any = 'black',
        transition_time: float=1
    ) -> Point:
        x = LerpValue(self.x0, self.x1, transition_time)
        y = LerpValue(self.y0, self.y1, transition_time)
        return Point(x, y, radius, stroke, color, fill)

    def get_length(self) -> float:
        dx = self.start[0] - self.end[0]
        dy = self.start[1] - self.end[1]
        return math.hypot(dx, dy)

    def attach(self, graph: Graph) -> Line:
        self.graph = graph

        if isinstance(self.start, Point): self.x0, self.y0 = self.start.x, self.start.y
        else: self.x0, self.y0 = self.start
        if isinstance(self.end, Point): self.x1, self.y1 = self.end.x, self.end.y
        else: self.x1, self.y1 = self.end

        self.x0, self.y0 = get_value(self.x0), get_value(self.y0)
        self.x1, self.y1 = get_value(self.x1), get_value(self.y1)

        if self.transition_time == 0: return self
        self.x = LerpValue(self.x0, self.x1, self.transition_time, self.start_time)
        self.y = LerpValue(self.y0, self.y1, self.transition_time, self.start_time)
        return self

    def show_cross_surface(self) -> None:
        x0, y0 = self.x0.get(), self.y0.get()
        if self.transition_time > 0: x1, y1 = self.x.get(), self.y.get()
        else: x1, y1 = self.x1.get(), self.y1.get()

        start = [self.start.graph.grid.convert_x_to_pixel(x0), self.start.graph.grid.convert_y_to_pixel(y0)]
        end = [self.end.graph.grid.convert_x_to_pixel(x1), self.end.graph.grid.convert_y_to_pixel(y1)]

        start[0] += self.start.graph.x
        start[1] += self.start.graph.y
        end[0] += self.end.graph.x
        end[1] += self.end.graph.y
        
        pygame.draw.line(self.graph.screen, self.color.rgb(), start, end, width=self.stroke)

    def show(self) -> None:
        if self.cross_surface: return self.show_cross_surface()

        x0, y0 = self.x0.get(), self.y0.get()
        if self.transition_time > 0: x1, y1 = self.x.get(), self.y.get()
        else: x1, y1 = self.x1.get(), self.y1.get()

        surface = self.graph.surface
        start = [self.graph.grid.convert_x_to_pixel(x0), self.graph.grid.convert_y_to_pixel(y0)]
        end = [self.graph.grid.convert_x_to_pixel(x1), self.graph.grid.convert_y_to_pixel(y1)]
        
        pygame.draw.line(surface, self.color.rgb(), start, end, width=self.stroke)


class Lines:
    def __init__(
        self, points: tuple[tuple[unit, unit]|Point],
        color: any='white', fill: any=None,
        stroke: pixel=1, closed: bool=True,
        transition_time: float=0, start_time: float=0
    ):
        self.points = []
        for point in points:
            if isinstance(point, Point): self.points.append(point)
            else: self.points.append(Point(*point))

        if closed: self.points.append(self.points[0])
        self.fill = get_color(fill)
        self.color = get_color(color)
        self.stroke = get_value(stroke)
        self.transition_time = transition_time
        self.start_time = start_time
    
    def point_along(
        self,
        radius: pixel = 10, stroke: pixel = 3,
        color: any = 'white', fill: any = 'black',
        transition_time: float=1
    ) -> Point:
        ...

    def attach(self, graph: Graph) -> None:
        total_length = 0
        for i, point in enumerate(self.points[:-1]):
            total_length += point.distance_to(self.points[i+1])

        start_time = self.start_time
        for a, b in zip(self.points[:-1], self.points[1:]):
            length = a.distance_to(b)
            transition_time = self.transition_time * length / total_length

            graph.add(Line(a, b, self.color, self.width, transition_time, start_time))
            start_time += transition_time
    
    def show(self) -> None:
        ...