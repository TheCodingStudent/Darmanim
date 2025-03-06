from __future__ import annotations
import pygame

from Darmanim.types import *

pygame.init()
iterable = (tuple, list)


def parse_base(value: float, base: tuple[str, int], decimals: int=3) -> str:
    value /= base[1]
    if value == 0: return '0'
    if value % 1: return f'{round(value, decimals)}{base[0]}'
    if value == 1: return base[0]
    if value == -1: return f'-{base[0]}'
    return f'{int(value)}{base[0]}'


def parse_time_to_sec(time: str|int|float) -> float:
    if isinstance(time, (int|float)): return time
    minutes, seconds = time.split(':')
    return 60*int(minutes) + float(seconds)


def parse_size(size: str|int|float, factor: float=1, cast=float) -> float:
    if isinstance(size, (int|float)): return size
    if size.endswith('%'): return cast(factor * float(size[:-1])/100)


class Clock:
    fps: int=0
    def __init__(self):
        self.dt: sec = 0
        self.time: sec = 0
        self.clock = pygame.time.Clock()
    
    def get_fps(self) -> float:
        return self.clock.get_fps()

    def tick(self) -> ms:
        self.dt = self.clock.tick(self.fps) / 1000
        self.time += self.dt

        return self.dt


class Object:
    elements: list[Object] = []
    clock: Clock = Clock()
    def __init__(self, transition_time: float|str=0, start_time: float|str=0):
        self.t = 0
        self.time = 0
        self.start_time = parse_time_to_sec(start_time)
        self.transition_time = parse_time_to_sec(transition_time)
    
    def update(self) -> bool:
        if self.time > self.transition_time + Object.clock.dt: Object.elements.remove(self)
        if Object.clock.time < self.start_time: return False
        self.time += Object.clock.dt
        self.t = min(self.time / self.transition_time, 1)
        return True

    def _update_all() -> None:
        Object.clock.tick()
        for element in Object.elements:
            element.update()


class Event:
    def __init__(self, function: callable, args: list[any]=[], kwargs: dict[str, any]={}, event_time: str|int=0):
        Object.elements.append(self)

        self.event_time = parse_time_to_sec(event_time)
        self.args = args
        self.kwargs = kwargs
        self.function = function

    def update(self) -> None:
        if Object.clock.time >= self.event_time:
            self.function(*self.args, **self.kwargs)
            Object.elements.remove(self)


class TransitionValue(Object):
    def __init__(self, start: any, end: any, transition_time: str|int, start_time: str|int=0):
        super().__init__()
        Object.elements.append(self)

        self.value = self.start = start
        self.end = end
    
    def update(self) -> None:
        super().update()