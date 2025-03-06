from __future__ import annotations
import pygame
import numpy as np
from Darmanim.window import Window
from Darmanim.globals import Object
from Darmanim.constants import TWO_PI
from Darmanim.color import Color, get_color


class Polygon:
    def __init__(self, points: np.array, color: Color|str, fill: Color|str|None, width: int, sort: bool=True):
        self.centroid = sum(points) / len(points)
        self.points = self.sort_points(points) if sort else points
        self.color = get_color(color)
        self.fill = get_color(fill)
        self.width = width

    def copy(self) -> Polygon:
        return Polygon(self.points, self.color, self.fill, self.width, False)

    def sort_points(self, points: np.array) -> np.array:
        atan = lambda row: np.atan2(*row) % TWO_PI
        shifted = points - self.centroid
        indices = np.apply_along_axis(atan, axis=1, arr=shifted).argsort()
        return points[indices]

    def update(self) -> None:
        self.draw()
    
    def attach(self, window: Window) -> Polygon:
        self.surface = window.surface
        Object.elements.append(self)
        return self

    def lerp(self, other: Polygon, t: float) -> Polygon:

        points = self.points + (other.points - self.points) * t
        color = self.color.lerp(other.color, t)
        fill = self.fill.lerp(other.fill, t) if self.fill is not None else None
        width = int(self.width + (other.width - self.width) * t)

        return Polygon(points, color, fill, width, False)

    def draw(self) -> None:
        if self.fill is not None:
            pygame.draw.polygon(self.surface, self.fill.rgba(), self.points)

        pygame.draw.polygon(self.surface, self.color.rgba(), self.points, width=self.width)
        # pygame.draw.circle(self.surface, 'red', self.centroid, 5)


class Circle(Polygon):
    def __init__(self, x: float, y: float, radius: float, color: Color|str='yellow', fill: Color|str|None=None, width: int=1):
        points = np.zeros((360, 2))
        radians = np.radians(np.arange(360))
        points[:, 0] = radius * np.cos(radians) + x
        points[:, 1] = radius * np.sin(radians) + y

        super().__init__(points, color, fill, width)


class Rectangle(Polygon):
    def __init__(self, x: float, y: float, w: float, h: float, color: Color|str='yellow', fill: Color|str|None=None, width: int=1):

        points = np.zeros((360, 2))
        arange = np.arange(-0.5, 0.5 + 1/89, 1/89)
        points[:90, 0] = points[180:270, 0] = w * arange + x
        points[90:180, 1] = points[270:, 1] = h * arange + y
        points[:90, 1] = y - h/2
        points[90:180, 0] = x + w/2
        points[180:270, 1] = y + h/2
        points[270:, 0] = x - w/2

        super().__init__(points, color, fill, width)