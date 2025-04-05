from __future__ import annotations
import math
import pygame
import numpy as np
from Darmanim.color import get_color
from Darmanim.graph import Graph, Point, unit, pixel
from Darmanim.values import get_value, LerpValue, ContinuosValue, Action, Event, LerpEvent


type degrees = float


class Polygon:
    def __init__(self, points: list[tuple[float, float]], x: unit=None, y: unit=None, color: any='white', fill: any=None, stroke: pixel=1):
        self.points = np.array(points)
        self.x = get_value(x)
        self.y = get_value(y)
        self.fill = get_color(fill)
        self.color = get_color(color)
        self.stroke = get_value(stroke)

    def set_stroke(self, stroke: pixel, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.stroke = stroke
            else: LerpEvent(self, 'stroke', self.stroke, stroke, transition_time, 0, True)
        else: Action(self.set_stroke, start_time, args=(stroke, 0, transition_time))

        return self
    
    def set_color(self, color: unit, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.color = get_color(color)
            else: LerpEvent(self, 'color', self.color, get_color(color), transition_time, 0, True)
        else: Action(self.set_color, start_time, args=(color, 0, transition_time))

        return self

    def get_points(self, radius: pixel=10, stroke: pixel=3, color: any='white', fill: any='black') -> list[Point]:
        return Point.from_list(self.points, radius, stroke, color, fill)

    def update(self) -> None:
        if not hasattr(self, 'graph'): return
        x = self.graph.grid.convert_x_to_pixel(self.points[:, 0])
        y = self.graph.grid.convert_y_to_pixel(self.points[:, 1])
        self.coordinates = np.column_stack((x, y))

    def attach(self, graph: Graph) -> Polygon:
        self.graph = graph
        self.update()
        return self

    def show(self) -> None:
        self.update()
        if self.fill: pygame.draw.polygon(self.graph.surface, self.fill.rgb(), self.coordinates)
        if self.stroke == 1:
            return pygame.draw.aalines(self.graph.surface, self.color.rgb(), True, self.coordinates)
        else: pygame.draw.polygon(self.graph.surface, self.color.rgb(), self.coordinates, width=self.stroke)


class RegularPolygon(Polygon):
    def __init__(
        self,
        x: unit, y: unit,
        radius: unit, sides: int,
        color: any='white', fill: any=None,
        phase: any=0,
        stroke: pixel=1
    ):
        self.phase = get_value(phase)
        self.sides = get_value(sides)
        self.radius = get_value(radius)
        super().__init__([], x, y, color, fill, stroke)
        self.update()
    
    def update(self) -> None:
        self.offset = 1.5*np.pi - np.pi/self.sides
        self.points = np.zeros((180, 2))
        phase = self.phase + self.offset
        d_angle = 2*np.pi/self.sides

        for i in range(self.sides.get(int)):
            a = int(180 * i /  self.sides)
            b = int(180 * (i + 1) /  self.sides)
            self.points[a:b, 0] = self.x + math.cos(d_angle * i + phase) * self.radius
            self.points[a:b, 1] = self.y + math.sin(d_angle * i + phase) * self.radius
        
        self.points[b:, 0] = self.x + math.cos(d_angle * (i + 1) + phase) * self.radius
        self.points[b:, 1] = self.y + math.sin(d_angle * (i + 1) + phase) * self.radius

        super().update()
    
    def get_points(self, radius: pixel=10, stroke: pixel=3, color: any='white', fill: any='black') -> list[Point]:
        result = []

        self.offset = 1.5*np.pi - np.pi/self.sides
        phase = self.phase + self.offset
        d_angle = 2*np.pi/self.sides

        for i in range(self.sides.get(int)):
            x = self.x + math.cos(d_angle * i + phase) * self.radius
            y = self.y + math.sin(d_angle * i + phase) * self.radius
            result.append(Point(x, y, radius, stroke, color, fill))
        
        if self.sides.get() % 1 == 0: return result
        x = self.x + math.cos(d_angle * (i + 1) + phase) * self.radius
        y = self.y + math.sin(d_angle * (i + 1) + phase) * self.radius
        result.append(Point(x, y, radius, stroke, color, fill))

        return result


class Ellipse(Polygon):
    def __init__(
        self,
        center: tuple[unit, unit]|Point, a: float, b: float,
        color: any='white', fill: any=None,
        stroke: int=1
    ):
        if isinstance(center, Point): x, y = center.x, center.y
        else: x, y = center
        super().__init__([], x, y, color, fill, stroke)
        self.a = get_value(a)
        self.b = get_value(b)
        self.update()
    
    def set_minor_radius(self, radius: unit, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.b = radius
            else: LerpEvent(self, 'b', self.b, radius, transition_time, 0, True)
        else: Action(self.set_minor_radius, start_time, args=(radius, 0, transition_time))

        return self
    
    def set_major_radius(self, radius: unit, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.a = radius
            else: LerpEvent(self, 'a', self.a, radius, transition_time, 0, True)
        else: Action(self.set_major_radius, start_time, args=(radius, 0, transition_time))

        return self

    def update(self) -> None:
        angles = np.arange(0, 2*np.pi, 2*np.pi/180)
        self.points = np.zeros((180, 2))
        self.points[:, 0] = self.a * np.cos(angles) + self.x.get()
        self.points[:, 1] = self.b * np.sin(angles) + self.y.get()
        super().update()
    
    def point_along(self, start_angle: degrees, end_angle: degrees, transition_time: float=1) -> Point:
        start_angle = math.radians(start_angle)
        end_angle = math.radians(end_angle)

        x_func = lambda x: math.cos(x) * self.a + self.x
        y_func = lambda x: math.sin(x) * self.b + self.y
        x = LerpValue(start_angle, end_angle, transition_time, function=x_func)
        y = LerpValue(start_angle, end_angle, transition_time, function=y_func)
        return Point(x, y)


class Circle(Ellipse):
    def __init__(
        self,
        center: tuple[unit, unit]|Point, radius: float,
        color: any='white', fill: any=None,
        stroke: int=1
    ):
        self.radius = get_value(radius)
        super().__init__(center, radius, radius, color, fill, stroke)
    
    def set_radius(self, radius: unit, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.radius = radius
            else: LerpEvent(self, 'radius', self.radius, radius, transition_time, 0, True)
        else: Action(self.set_radius, start_time, args=(radius, 0, transition_time))

        return self

    def update(self) -> None:
        self.a = self.b = self.radius
        super().update()

    def point_along(
        self,
        start_angle: degrees, end_angle: degrees|None=None,
        color: any='white', fill: any=None, 
        radius: pixel=10, stroke: pixel=3,
        transition_time: float=1,
        direction: int=1, graph: Graph|None=None
    ) -> Point:
        start_angle = math.radians(start_angle)

        x_func = lambda x: math.cos(x) * self.radius + self.x
        y_func = lambda x: math.sin(x) * self.radius + self.y

        if end_angle is None:
            x = ContinuosValue(start_angle, 2*np.pi*direction, transition_time, function=x_func)
            y = ContinuosValue(start_angle, 2*np.pi*direction, transition_time, function=y_func)
        else:
            end_angle = math.radians(end_angle)
            x = LerpValue(start_angle, end_angle, transition_time, function=x_func)
            y = LerpValue(start_angle, end_angle, transition_time, function=y_func)

        point = Point(x, y, radius, stroke, color, fill)
        if graph is not None: point.graph = graph

        return point


class Rectangle(Polygon):
    def __init__(
        self,
        x: float, y: float,
        width: float, height: float,
        color: any='white', fill: any=None,
        stroke: int=1
    ):
        super().__init__([], x, y, color, fill, stroke)
        self.width = get_value(width)
        self.height = get_value(height)
    
    def set_width(self, width: unit, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.width = width
            else: LerpEvent(self, 'width', self.width, width, transition_time, 0, True)
        else: Action(self.set_width, start_time, args=(width, 0, transition_time))

        return self

    def set_height(self, height: unit, start_time: float=0, transition_time: float=0) -> Circle:
        if start_time == 0:
            if transition_time == 0: self.height = height
            else: LerpEvent(self, 'height', self.height, height, transition_time, 0, True)
        else: Action(self.set_height, start_time, args=(height, 0, transition_time))

        return self

    def point_along(self, start_angle: degrees, end_angle: degrees, transition_time: float=1) -> Point:
        fisrt_angle = math.atan(self.height / self.width)
        complementary_angle = math.pi/2 - fisrt_angle

        return Point(0, 0)

    def get_points(self, radius: pixel=10, stroke: pixel=3, color: any='white', fill: any='black') -> list[Point]:
        corners = [
            (self.x - self.width/2, self.y - self.height/2),
            (self.x + self.width/2, self.y - self.height/2),
            (self.x + self.width/2, self.y + self.height/2),
            (self.x - self.width/2, self.y + self.height/2),
        ]
        return Point.from_list(corners, radius, stroke, color, fill)

    def update(self) -> None:
        self.points = np.zeros((180, 2))
        x_range = self.x + np.arange(-0.5, 0.5 + 1/45, 1/44) * self.width
        y_range = self.y + np.arange(-0.5, 0.5 + 1/45, 1/44) * self.height
        self.points[45:90, 0], self.points[135:, 0] = self.x + self.width/2, self.x - self.width/2
        self.points[:45, 1], self.points[90:135, 1] = self.y - self.height/2, self.y + self.height/2
        self.points[:45, 0] = self.points[90:135, 0][::-1] = x_range
        self.points[45:90, 1] = self.points[135:, 1][::-1] = y_range
        super().update()


class Square(Rectangle):
    def __init__(
        self,
        x: float, y: float, side: float,
        color: any='white', fill: any=None,
        stroke: int=1
    ):
        super().__init__(x, y, side, side, color, fill, stroke)