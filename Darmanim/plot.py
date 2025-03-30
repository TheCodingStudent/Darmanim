from __future__ import annotations
import pygame
from Darmanim.window import Window
from Darmanim.color import get_color
from Darmanim.graph import Grid, Axis
from Darmanim.values import get_value

type coordinate = list[tuple[float, float]]


class PlotPoint:
    def __init__(self, group: ScatterGroup|PlotGroup|None=None, x: any=None, y: any=None, color: any='white', radius: int=5):
        self.group = group
        self.x = get_value(x)
        self.y = get_value(y)

        self.color = get_color(color)
        self.radius = get_value(radius)

        self.update()
    
    def get(self) -> tuple[float, float]:
        return self.center

    def update(self) -> None:
        if not self.group: return
        if self.x is not None: x = self.group.plot.grid.convert_x_to_pixel(self.x.get())
        if self.y is not None: y = self.group.plot.grid.convert_y_to_pixel(self.y.get())
        self.center = (x, y)

    def style(self, surface: pygame.Surface, center: tuple[float, float], radius: int, color: tuple[int, int, int]):
        pygame.draw.circle(surface, color, center, radius)

    def show(self) -> None:
        self.style(self.group.plot.surface, self.center, self.radius.get(int), self.color.rgb())
    
    def __call__(self, *args, **kwargs) -> PlotPoint:
        group, x, y = args
        return PlotPoint(group, x, y, self.color, self.radius)


class Plot:
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

        self.groups = []
    
    def draw_border(self) -> None:
        if (self.border is None) or (self.border_width == 0): return
        pygame.draw.rect(self.surface, self.border.rgb(), (0, 0, self.width, self.height), width=self.border_width)

    def attach(self, window: Window, x: int|None=None, y: int|None=None) -> None:
        self.screen = window.screen
        if self.color is None: self.color = window.color
        if x is None: self.x = (self.screen.get_width() - self.width) / 2
        else: self.x = x
        if y is None: self.y = (self.screen.get_height() - self.height) / 2
        else: self.y = y

    def show(self) -> None:
        self.surface.fill(self.color.rgb())

        self.grid.show()
        self.axis.show()

        for group in self.groups:
            group.update()
            group.show()

        self.draw_border()
        self.screen.blit(self.surface, (self.x, self.y))
    
    def scatter(
        self, coordinates: list[tuple[float, float]],
        color: any='white', radius: int=3,
        call_update: bool=False,
        plot_style: any=PlotPoint
    ) -> None:
        group = ScatterGroup(self, coordinates, color, radius, call_update, plot_style)
        self.groups.append(group)
    
    def plot(
        self, coordinates: list[tuple[float, float]],
        color: any='white', fill: any=None,
        closed: bool=True, width: int=1, radius: int=3,
        call_update: bool=False,
        plot_style: any=PlotPoint
    ) -> None:
        group = PlotGroup(self, coordinates, color, fill, closed, width, radius, call_update, plot_style)
        self.groups.append(group)


class ScatterGroup:
    def __init__(
        self, plot: Plot,
        coordinates: list[tuple[float, float]],
        color: any, radius: int,
        call_update: bool, plot_style: any
    ):
        self.plot = plot
        if isinstance(plot_style, type(lambda x: x)):
            self.coordinates = []
            for coord in coordinates:
                self.coordinates.append(PlotPoint(self, *coord, color, radius))
                self.coordinates[-1].style = plot_style
        else: self.coordinates = [plot_style(self, *coord, color, radius) for coord in coordinates]

        self.call_update = call_update
        self.update(update_values=True)
    
    def update(self, update_values: bool=False) -> None:
        if not (self.call_update or update_values): return
        for coord in self.coordinates: coord.update()

    def show(self) -> None:
        for coord in self.coordinates: coord.show()


class PlotGroup(ScatterGroup):
    def __init__(
        self,
        plot: Plot, coordinates: list[tuple[float, float]],
        color: any, fill: any,
        closed: bool, width: int, radius: int,
        call_update: bool,
        plot_style: any
    ):
        super().__init__(plot, coordinates, color, radius, call_update, plot_style)
        self.lines = []
        self.closed = closed
        self.width = get_value(width)

        self.fill = get_color(fill) if len(coordinates) >= 3 else None
        self.color = get_color(color)

    def update(self, update_values: bool=False) -> None:
        super().update(update_values)
        if len(self.coordinates) < 2: return
        self.lines = [coord.get() for coord in self.coordinates]

    def show(self) -> None:
        if self.fill: pygame.draw.polygon(self.plot.surface, self.fill.rgb(), self.lines)
        pygame.draw.lines(self.plot.surface, self.color.rgb(), self.closed, self.lines, width=self.width.get(int))
        super().show()