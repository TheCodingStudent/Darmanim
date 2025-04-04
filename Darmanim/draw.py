from __future__ import annotations
import math
import pygame
import numpy as np
from Darmanim.time import Clock
from Darmanim.window import Surface
from Darmanim.color import get_color, LerpColor
from Darmanim.values import get_value, get_values, Value, LerpValue, LerpEventGroup, Action

type pixel = float
type rect = tuple[pixel, pixel, pixel, pixel]
type coordinate = tuple[pixel, pixel]


class Line:
    def __init__(
        self, surface: Surface,
        start: coordinate, end: coordinate,
        color: any='white', stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.x0, self.y0 = get_values(start)
        self.x1, self.y1 = get_values(end)
        self.stroke = get_value(stroke)
        self.color = get_color(color)
        self.start_time = start_time

        surface.add_element(self, z_index)
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        start, end = (self.x0.get(), self.y0.get()), (self.x1.get(), self.y1.get())
        pygame.draw.line(self.surface.screen, self.color.rgb(), start, end, self.stroke.get(int))


class Lines:
    def __init__(
        self, surface: Surface,
        points: list[coordinate], color: any='white',
        closed: bool=False, stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.points = [get_values(point) for point in points]
        self.closed = closed
        self.color = get_color(color)
        self.stroke = get_value(stroke)
        self.start_time = start_time

        f = lambda p: type(p[0]) != Value or type(p[1]) != Value
        self.should_update = any(map(f, self.points)) 

        self.update(update_values=True)
        surface.add_element(self, z_index)
    
    def update(self, update_values: bool=False) -> None:
        if not update_values:
            if Clock.time < self.start_time or not self.should_update: return
        self.coordinates = [(x.get(), y.get()) for x, y in self.points]
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        pygame.draw.lines(self.surface.screen, self.color.rgb(), self.closed, self.coordinates, self.stroke.get(int))


class Circle:
    def __init__(
        self, surface: Surface,
        center: tuple[pixel, pixel], radius: pixel,
        color: any='white', stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.x, self.y = get_values(center)
        self.radius = get_value(radius)
        self.color = get_color(color)
        self.stroke = get_value(stroke)

        self.should_update = type(self.x) != Value or type(self.y) != Value
        self.start_time = start_time

        self.update(update_values=True)
        surface.add_element(self, z_index)
    
    def update(self, update_values: bool=False) -> None:
        if not update_values:
            if Clock.time < self.start_time or not self.should_update: return
        self.center = (self.x.get(), self.y.get())
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        pygame.draw.circle(self.surface.screen, self.color.rgb(), self.center, self.radius.get(), self.stroke.get(int))


class Ellipse:
    def __init__(
        self, surface: Surface,
        center: tuple[pixel, pixel], rx: pixel, ry: pixel,
        color: any='white', stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.x, self.y = get_values(center)
        self.rx, self.ry = get_value(rx), get_value(ry)
        self.color = get_color(color)
        self.stroke = get_value(stroke)

        self.should_update = type(self.x) != Value or type(self.y) != Value or type(self.rx) != Value or type(self.ry) != Value
        self.start_time = start_time

        self.update(update_values=True)
        surface.add_element(self, z_index)
    
    def update(self, update_values: bool=False) -> None:
        if not update_values:
            if Clock.time < self.start_time or not self.should_update: return
        rx, ry = self.rx.get(), self.ry.get()
        self.rect = (self.x.get()-rx, self.y.get()-ry, 2*rx, 2*ry)
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        pygame.draw.ellipse(self.surface.screen, self.color.rgb(), self.rect, self.stroke.get(int))


class Rectangle:
    def __init__(
        self, surface: Surface,
        rectangle: rect, color: any='white', stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.x, self.y, self.w, self.h = rectangle
        self.color = color
        self.stroke = stroke

        self.should_update = type(self.x) != Value or type(self.y) != Value or type(self.w) != Value or type(self.h) != Value
        self.start_time = start_time

        self.update(update_values=True)
        surface.add_element(self, z_index)
    
    def update(self, update_values: bool=False) -> None:
        if not update_values:
            if Clock.time < self.start_time or not self.should_update: return
        self.rect = (self.x.get(), self.y.get(), self.w.get(), self.h.get())
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        pygame.draw.rect(self.surface.screen, self.color.rgb(), self.rect, self.stroke.get(int))

    def __setattr__(self, name: str, value: any):
        if name in ('x', 'y', 'w', 'h', 'stroke'): return super().__setattr__(name, get_value(value))
        if name == 'color': return super().__setattr__(name, get_color(value))
        return super().__setattr__(name, value)


class Polygon:
    def __init__(
        self, surface: Surface,
        points: list[coordinate], color: any='white', stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.points = [get_values(point) for point in points]

        self.color = get_color(color)
        self.stroke = get_value(stroke)

        f = lambda p: type(p[0]) != Value or type(p[1]) != Value
        self.should_update = any(map(f, self.points))
        self.start_time = start_time

        self.update(update_values=True)
        surface.add_element(self, z_index)
    
    def update(self, update_values: bool=False) -> None:
        if not update_values:
            if Clock.time < self.start_time or not self.should_update: return
        self.coordinates = [(x.get(), y.get()) for x, y in self.points]
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        pygame.draw.polygon(self.surface.screen, self.color.rgb(), self.coordinates, self.stroke.get(int))


class Arc:
    def __init__(self, surface: Surface, start: coordinate, end: coordinate, radius: pixel, color: any='white', stroke: pixel=1, flip_orientation: bool=False, flip_direction: bool=False, z_index: int=9999):
        self.surface = surface
        self.start = get_values(start)
        self.end = get_values(end)
        self.radius = get_value(radius)
        self.color = get_color(color)
        self.stroke = get_value(stroke)

        self.flip_orientation = flip_orientation
        self.flip_direction = flip_direction

        self.should_update = True
        self.update()

        surface.add_element(self, z_index)
    
    def update(self) -> None:
        if not self.should_update: return

        a = self.start[0].get(), self.start[1].get()
        b = self.end[0].get(), self.end[1].get()
        r = self.radius.get()

        m = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        t = b[0] - a[0], b[1] - a[1]
        n = b[1] - a[1], a[0] - b[0]
        dn = math.hypot(*n)
        d = math.hypot(*t)

        h = math.sqrt(r*r - d*d/4)

        if not self.flip_orientation: o = m[0] - h*n[0]/dn, m[1] - h*n[1]/dn
        else: o = m[0] + h*n[0]/dn, m[1] + h*n[1]/dn 

        av = a[0] - o[0], a[1] - o[1]
        bv = b[0] - o[0], b[1] - o[1]

        if not self.flip_direction: av, bv = bv, av

        self.rect = (o[0] - r, o[1] - r, 2*r, 2*r)
        self.start_angle = math.atan2(-av[1], av[0])
        self.end_angle = math.atan2(-bv[1], bv[0])
    
    def show(self) -> None:
        pygame.draw.arc(self.surface.screen, self.color.rgb(), self.rect, self.start_angle, self.end_angle, width=self.stroke.get(int))



class AnimatedArc:
    def __init__(
        self, surface: Surface,
        start: coordinate, end: coordinate, radius: pixel,
        color: any='white', stroke: pixel=1,
        transition_time: float=1, start_time: float=0,
        flip_orientation: bool=False, flip_direction: bool=False,
        z_index: int=9999
    ):
        self.surface = surface
        self.start = get_values(start)
        self.end = get_values(end)
        self.radius = get_value(radius)
        self.color = get_color(color)
        self.stroke = get_value(stroke)

        self.t = LerpValue(0, 1, transition_time, start_time)

        self.flip_orientation = flip_orientation
        self.flip_direction = flip_direction

        self.should_update = True

        surface.add_element(self, z_index)
    
    def update(self) -> None:
        if not self.should_update: return

        a = self.start[0].get(), self.start[1].get()
        b = self.end[0].get(), self.end[1].get()
        r = self.radius.get()

        m = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        t = b[0] - a[0], b[1] - a[1]
        n = b[1] - a[1], a[0] - b[0]
        dn = math.hypot(*n)
        d = math.hypot(*t)

        h = math.sqrt(r*r - d*d/4)

        if not self.flip_orientation: o = m[0] - h*n[0]/dn, m[1] - h*n[1]/dn
        else: o = m[0] + h*n[0]/dn, m[1] + h*n[1]/dn 

        av = a[0] - o[0], a[1] - o[1]
        bv = b[0] - o[0], b[1] - o[1]

        if not self.flip_direction: av, bv = bv, av

        self.rect = (o[0] - r, o[1] - r, 2*r, 2*r)
        self.start_angle = math.atan2(-av[1], av[0])
        self.end_angle = math.atan2(-bv[1], bv[0])

        self.end_angle = self.start_angle + (self.end_angle - self.start_angle) * self.t.get()
    
    def show(self) -> None:
        self.update()
        pygame.draw.arc(self.surface.screen, self.color.rgb(), self.rect, self.start_angle, self.end_angle, width=self.stroke.get(int))


class RegularPolygon(Polygon):
    def __init__(
        self, surface: Surface,
        center: tuple[pixel, pixel], radius: pixel,
        sides: float, phase: float=0,
        color: any='white', stroke: pixel=1,
        start_time: float=0, z_index: int=9999
    ):
        self.x, self.y = get_values(center)
        self.radius = get_value(radius)
        self.sides = get_value(sides)
        self.phase = get_value(phase)
        self.should_update = type(self.sides) != Value or type(self.x) != Value or type(self.y) != Value or type(self.radius) != Value
        super().__init__(surface, [], color, stroke, start_time, z_index)

    def update(self, update_values: bool=False) -> None:
        if not update_values:
            if Clock.time < self.start_time or not self.should_update: return

        offset = 1.5*math.pi - math.pi/self.sides
        self.coordinates = np.zeros((180, 2))
        phase = self.phase.get() + offset
        d_angle = 2*math.pi/self.sides

        for i in range(self.sides.get(int)):
            a = int(180 * i /  self.sides)
            b = int(180 * (i + 1) /  self.sides)
            self.coordinates[a:b, 0] = self.x.get() + math.cos(d_angle * i + phase) * self.radius.get()
            self.coordinates[a:b, 1] = self.y.get() + math.sin(d_angle * i + phase) * self.radius.get()
        
        self.coordinates[b:, 0] = self.x.get() + math.cos(d_angle * (i + 1) + phase) * self.radius.get()
        self.coordinates[b:, 1] = self.y.get() + math.sin(d_angle * (i + 1) + phase) * self.radius.get()


class AnimatedLine:
    def __init__(
        self, surface: Surface,
        start: coordinate, end: coordinate,
        color: any='white', stroke: pixel=1,
        transition_time: float=1, start_time: float=0,
        z_index: int=9999
    ):
        self.surface = surface
        self.x0, self.y0 = get_values(start)
        self.x1, self.y1 = get_values(end)
        self.x = LerpValue(self.x0, self.x1, transition_time, start_time)
        self.y = LerpValue(self.y0, self.y1, transition_time, start_time)

        self.stroke = get_value(stroke)
        self.color = get_color(color)
        self.start_time = start_time

        surface.add_element(self, z_index)
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        start, end = (self.x0.get(), self.y0.get()), (self.x.get(), self.y.get())
        pygame.draw.line(self.surface.screen, self.color.rgb(), start, end, self.stroke.get(int))


class AnimatedLines:
    def __init__(
        self, surface: Surface,
        points: list[coordinate], color: any='white',
        closed: bool=False, stroke: pixel=1,
        transition_time: float=1, start_time: float=0,
        z_index: int=9999
    ):

        accumulated_lengths = [0]
        if closed: points = list(points) + [points[0]]
        for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
            accumulated_lengths.append(math.hypot(x1 - x0, y1 - y0) + accumulated_lengths[-1])
        
        self.t_values = [length/accumulated_lengths[-1] for length in accumulated_lengths]

        self.surface = surface
        self.points = points
        self.color = get_color(color)
        self.stroke = get_value(stroke)
        self.start_time = start_time
        self.transition_time = transition_time

        surface.add_element(self, z_index)

    def draw_line(self, index: int) -> None:
        time_t = (Clock.time - self.start_time) / self.transition_time - self.t_values[index]
        if time_t < 0: return

        total_t = self.t_values[index+1] - self.t_values[index]
        t = time_t / total_t
        (x0, y0), (x1, y1) = self.points[index], self.points[index + 1]

        if t >= 1:
            return pygame.draw.line(self.surface.screen, self.color.rgb(), (x0, y0), (x1, y1), self.stroke.get(int))
        
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        pygame.draw.line(self.surface.screen, self.color.rgb(), (x0, y0), (x, y), self.stroke.get(int))

    def show(self) -> None:
        if Clock.time < self.start_time: return

        for i in range(len(self.points) - 1):
            self.draw_line(i)


class Group:
    def __init__(self, elements: list[any]):
        self._elements = elements
        self.n = len(self._elements)
    
    def __setattr__(self, name: str, value: any) -> None:
        if name in ('_elements', 'n'): return super().__setattr__(name, value) 
        if isinstance(value, (tuple, list)):
            for i, val in enumerate(value[:self.n]): setattr(self._elements[i], name, val)
        else:
            for i, element in enumerate(self._elements): setattr(element, name, value)
    
    def __getattribute__(self, name):
        if name in ('_elements', 'n'): return super().__getattribute__(name)
        return Group([getattr(element, name) for element in self._elements])
    
    def __call__(self, *args, **kwargs) -> None:
        for element in self._elements:
            element(*args, **kwargs)

    def __getitem__(self, index: int|slice|str) -> any:
        if isinstance(index, slice):
            return Group(self._elements[index])
        if isinstance(index, str):
            return Group([letter for letter in self._elements if letter.font_text in index])
        return self._elements[index]


class Letter:
    def __init__(
        self, surface: Surface,
        text: str, x: float, y: float,
        size: int, color: any='white', font: str='cmuserifroman',
        start_time: float=0
    ):
        self.surface = surface
        self.font_text = text
        self.font_name = font
        self.font_size = size

        self.x, self.y = x, y
        self.color = color
        self.start_time = start_time

        self.should_update = True
        self.update(update_values=True)
    
    def update(self, update_values: bool=False) -> None:
        if not self.should_update: return

        if not update_values:
            if Clock.time < self.start_time: return

        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.text = self.font.render(self.font_text, True, self.color.rgb())
        # self.update_rect()
        self.rect = self.text.get_rect(topleft=(self.x.get(), self.y.get()))
    
    def update_rect(self) -> None:
        self.rect = self.text.get_rect(topleft=(self.x.get(), self.y.get()))
    
    def show(self) -> None:
        self.surface.screen.blit(self.text, self.rect)
    
    def __setattr__(self, name: str, value: any) -> None:
        if name == 'color':
            color = get_color(value)
            if not hasattr(self, 'color'):
                return super().__setattr__(name, color)
            if type(self.color) == LerpColor:
                return setattr(self.color, 'end', color)
            return super().__setattr__(name, color)

        elif name in 'xy': return super().__setattr__(name, get_value(value))
        super().__setattr__(name, value)


class Text:
    def __init__(
        self, surface: Surface,
        text: str|list[str], x: float, y: float,
        size: int, color: any='white', font: str='cmuserifroman',
        anchor_x: str='left', anchor_y: str='top',
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.size = size
        self.color = color
        self.font = font

        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

        self.z_index = z_index
        self.start_time = start_time

        self.letters = []
        self.length = 0
        self.start_x, self.start_y = x, y

        self.width, self.height = 0, 0
        self.x, self.y = float('inf'), float('inf')

        if isinstance(text, str): text = [text]
        for index, line in enumerate(text):
            self.parse_line(line, index, len(text))
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def parse_line(self, line: str, line_index: int, lines_number: int) -> None:
        width = 0
        x = self.start_x
        height = pygame.font.SysFont(self.font, self.size).get_height()

        for letter in line:
            self.letters.append(Letter(self.surface, letter, x, self.start_y+height*line_index, self.size, self.color, self.font, self.start_time))
            width += self.letters[-1].rect.width
            x = self.start_x + width
            self.length += 1
        
        self.width = max(self.width, width)
        self.height = height * lines_number 
        
        offset_x = 0
        if self.anchor_x == 'centerx': offset_x = -width/2
        elif self.anchor_x == 'right': offset_x = -width

        offset_y = 0
        if self.anchor_y == 'centery': offset_y = -self.height/2
        elif self.anchor_y == 'bottom': offset_y = -self.height

        self.x = min(self.x, self.start_x + offset_x)
        self.y = min(self.y, self.start_y + offset_y)

        for letter in self.letters[-len(line):]:
            letter.x += offset_x
            letter.y += offset_y
        
        self.surface.add_element(self, self.z_index)

    def displace_by(self, dx: pixel, dy: pixel, start_time: float=0, transition_time: float=0) -> Text:
        if start_time == 0:
            if transition_time == 0:
                for letter in self.letters:
                    letter.x += dx
                    letter.y += dy
            else:
                def update_function() -> None:
                    for letter in self.letters: letter.update_rect()

                starts_x = [letter.x for letter in self.letters]
                ends_x = [letter.x + dx for letter in self.letters]
                starts_y = [letter.y for letter in self.letters]
                ends_y = [letter.y + dy for letter in self.letters]
                LerpEventGroup(self.letters, ['x']*self.length, starts_x, ends_x, transition_time, update_elements=True, update_function=update_function)
                LerpEventGroup(self.letters, ['y']*self.length, starts_y, ends_y, transition_time, update_elements=True, update_function=update_function)
        else:
            Action(self.displace_by, start_time, args=(dx, dy, 0, transition_time))
        
        return self

    def update(self, update_values: bool=False) -> None:
        for letter in self.letters: letter.update()
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        for letter in self.letters: letter.show()
        pygame.draw.rect(self.surface.screen, 'white', self.rect, width=1)
    
    def __getitem__(self, index: int|slice|str) -> Letter:
        if isinstance(index, slice):
            return Group(self.letters[index])
        if isinstance(index, str):
            n = len(index)
            if n == 1:
                return Group([letter for letter in self.letters if letter.font_text == index])
            return Group([Group(self.letters[i:i+n]) for i in range(self.length - n + 1) if self.font_text[i:i+n] == index])

        return self.letters[index]
    

class AnimatedText(Text):
    def __init__(
        self, surface: Surface,
        text: str, x: float, y: float,
        size: int, color: any='white', font: str='cmuserifroman',
        anchor_x: str='left', anchor_y: str='top',
        transition_time: float=1, start_time: float=0,
        z_index: int=9999
    ):
        super().__init__(surface, text, x, y, size, color, font, anchor_x, anchor_y, start_time, z_index)

        transition_time /= self.length
        for letter in self.letters:
            letter.color = LerpColor(surface.color, letter.color, transition_time, start_time)
            start_time += transition_time
        
        self.transition_time = transition_time
        self.should_update = True

    def update(self, should_update: bool=False) -> None:
        if not self.should_update: return
        super().update(should_update)

        for i, letter in enumerate(self.letters):
            if Clock.time >= letter.start_time + i * self.transition_time + 0.1:
                letter.should_update = False
            else: break
        else: self.should_update = False


class FastText:
    def __init__(
        self, surface: Surface,
        text: str, x: float, y: float,
        size: int, color: any='white', font: str='cmuserifroman',
        anchor_x: str='left', anchor_y: str='top',
        start_time: float=0, z_index: int=9999
    ):
        self.surface = surface
        self.color = get_color(color)
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, self.color.rgb())
        self.rect = self.text.get_rect(**{anchor_x: x, anchor_y: y})
        self.start_time = start_time

        surface.add_element(self, z_index)
    
    def show(self) -> None:
        if Clock.time < self.start_time: return
        self.surface.screen.blit(self.text, self.rect)