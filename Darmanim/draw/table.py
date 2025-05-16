import pygame
from Darmanim.draw import Text, FastText
from Darmanim.time import Clock
from Darmanim.window import Surface
from Darmanim.color import get_color
from Darmanim.values import get_value

type pixel = float
type degrees = float
type rect = tuple[pixel, pixel, pixel, pixel]
type coordinate = tuple[pixel, pixel]


class Table:
    def __init__(
        self, surface: Surface,
        x: pixel, y: pixel,
        width: pixel, height: pixel,
        columns: int, rows: int,
        color: any='white', background: any=None,
        text_color: any='white', font: str='cmuserifroman', size: int=24,
        title: str='', header_height: pixel=0,
        stroke: pixel=1,
        start_time: float=0, z_index: int=9999,
    ):
        self.surface = surface
        self.x, self.y = x, y
        self.columns, self.rows = columns, rows
        self.width, self.height = width, height
        self.color = get_color(color)
        self.background = get_color(background)
        self.stroke = get_value(stroke)
        self.start_time = start_time
        self.z_index = z_index

        self.text_color = get_color(text_color)
        self.text_font = font
        self.text_size = size

        self.title = None
        self.header_height = header_height
        if title:
            self.title = Text(
                surface=self.surface, text=title,
                x=self.x + self.width/2, y=self.y,
                size=size, font=font, anchor_x='centerx', anchor_y='centery',
                start_time=start_time, background=background
            )
            if header_height == 0: self.header_height = self.title.height
            self.title.displace_by(dx=0, dy=self.header_height/2)
            self.height -= self.header_height
            self.y += self.header_height

        self.column_weights = [1 for _ in range(columns)]
        self.column_weight = columns
        self.row_weights = [1 for _ in range(rows)]
        self.row_weight = rows
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text_values = [['' for _ in range(columns)] for _ in range(rows)]
        self.values = [[None for _ in range(columns)] for _ in range(rows)]

        self.surface.add(self, start_time=start_time)
    
    def set_value(self, column: int, row: int, value: str) -> None:
        self.text_values[row][column] = value

        width = self.column_weights[column] / self.column_weight * self.width
        height = self.row_weights[row] / self.row_weight * self.height

        if column == 0: x = self.x + width/2
        else: x = self.x + sum(self.column_weights[:column]) / self.column_weight * self.width + width/2
        if row == 0: y = self.y + height/2
        else: y = self.y + sum(self.row_weights[:row]) / self.row_weight * self.height + height/2

        self.values[row][column] = FastText(
            surface=self.surface, text=value, x=x, y=y,
            size=self.text_size, color=self.text_color, font=self.text_font,
            anchor_x='centerx', anchor_y='centery', start_time=self.start_time, background=self.background
        )

    def set_column_weight(self, column: int, weight: float) -> None:
        self.column_weights[column] = weight
        self.column_weight = sum(self.column_weights)
    
    def set_row_weight(self, row: int, weight: float) -> None:
        self.row_weights[row] = weight
        self.row_weight = sum(self.row_weights)

    def show(self) -> None:
        if Clock.time < self.start_time: return

        pygame.draw.rect(self.surface.screen, self.color.rgb(), (self.x, self.y-self.header_height, self.width, self.header_height), width=self.stroke)

        y = self.y
        for i in range(self.rows):
            x = self.x
            height = self.row_weights[i] / self.row_weight * self.height
            for j in range(self.columns):
                width = self.column_weights[j] / self.column_weight * self.width
                rect = (x, y, width, height)
                pygame.draw.rect(self.surface.screen, self.color.rgb(), rect, width=self.stroke)
                x += width
            y += height

        pygame.draw.rect(self.surface.screen, self.color.rgb(), self.rect, width=self.stroke)
