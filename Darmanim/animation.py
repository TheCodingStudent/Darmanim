from __future__ import annotations
import math
import pygame
from Darmanim.globals import Object, Event


class CubicBezier:
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.p0 = pygame.Vector2(0, 0)
        self.p1 = pygame.Vector2(x1, y1)
        self.p2 = pygame.Vector2(x2, y2)
        self.p3 = pygame.Vector2(1, 1)
    
    def get(self, t: float) -> float:
        inverse = 1 - t
        result = (
            1 * (inverse ** 3) * self.p0            + 
            3 * (inverse ** 2) * self.p1 * t        + 
            3 * (inverse ** 1) * self.p2 * t ** 2   + 
            1 * (inverse ** 0) * self.p3 * t ** 3 
        )

        return result.y

    def __call__(self, t: float) -> float:
        return self.get(t)


class EaseIn:
    Linear = lambda x: x
    Sine = lambda x: 1 - math.cos(x * math.pi / 2)
    Cubic = lambda x: pow(x, 3)
    Quintic = lambda x: pow(x, 5)
    Circ = CubicBezier(0.55, 0, 1, 0.45)
    Back = CubicBezier(0.36, 0, 0.66, -0.56)
    Expo = CubicBezier(0.7, 0, 0.84, 0)


class EaseOut:
    Linear = lambda x: 1 - x
    Sine = lambda x: math.sin(x * math.pi / 2)
    Cubic = lambda x: 1 - pow(1 - x, 3)
    Quintic = lambda x: 1 - pow(1 - x, 5)
    Circ = CubicBezier(0, 0.55, 0.45, 1)
    Back = CubicBezier(0.34, 1.56, 0.64, 1)
    Expo = CubicBezier(0.16, 1, 0.3, 1)


class EaseInOut:
    Sine = lambda x: -(math.cos(x * math.pi) - 1) / 2
    Cubic = CubicBezier(0.65, 0, 0.35, 1)
    Quintic = CubicBezier(0.83, 0, 0.17, 1)
    Circ = CubicBezier(0.85, 0, 0.15, 1)
    Back = CubicBezier(0.68, -0.6, 0.32, 1.6)
    Expo = CubicBezier(0.87, 0, 0.13, 1)


class _AnimatedValue(Object):
    def __init__(
        self, element: any, attribute: str,
        start: any, end: any,
        transition_time: float|str, start_time: float|str,
        easing: CubicBezier|callable,
        update_function: callable|None=None
    ):
        super().__init__(transition_time, start_time)
        self.element = element
        self.attribute = attribute
        self.start = start
        self.end = end
        self.easing = easing
        self.update_function = update_function

    def update(self) -> None:
        if not super().update(): return

        t = self.easing(self.t)
        if hasattr(self.start, 'lerp'): value = self.start.lerp(self.end, t)
        else: value = self.start + (self.end - self.start) * t

        if self.update_function is not None: return self.update_function(value)
        setattr(self.element, self.attribute, value)


class _AnimatedObject(Object):
    def __init__(
        self, start: any, end: any,
        transition_time: float|str, start_time: float|str,
        easing: CubicBezier|callable
    ):
        super().__init__(transition_time, start_time)

        self.start = start
        self.current = start.copy()
        self.end = end
        self.easing = easing
    
    def update(self) -> None:
        if not super().update(): return

        t = self.easing(self.t)
        lerp = self.start.lerp(self.end, t)
        for name, value in lerp.__dict__.items():
            setattr(self.current, name, value)


def animate(
    element: any, attribute: str,
    end: any,
    transition_time: float|str, start_time: float|str=0,
    start: any=None,
    easing: CubicBezier|callable=EaseIn.Linear,
    update_function: callable|None=None
) -> any:
    if start is None: start = getattr(element, attribute)
    animation = _AnimatedValue(element, attribute, start, end, transition_time, start_time, easing, update_function)
    Object.elements.append(animation)
    return element


def fadeIn(
    element: any,
    transition_time: float|str, start_time: float|str=0,
    easing: CubicBezier|callable=EaseIn.Linear
) -> any:
    
    def inner(inner_element: any) -> None:
        color = inner_element.color
        animate(color, 'a', color.a, transition_time, start_time, 0, easing, color.update_alpha)

    Event(inner, args=(element, ), event_time=start_time)
    return element


def fadeOut(
    element: any,
    transition_time: float|str, start_time: float|str=0,
    easing: CubicBezier|callable=EaseIn.Linear
) -> any:
    
    def inner(inner_element: any) -> None:
        color = inner_element.color
        animate(color, 'a', 0, transition_time, start_time, color.a, easing, color.update_alpha)
    
    Event(inner, args=(element, ), event_time=start_time)
    return element


def transform(
    start: any, end: any,
    transition_time: float|str, start_time: float|str=0,
    easing: CubicBezier|callable=EaseIn.Linear
) -> any:
    animation = _AnimatedObject(start, end, transition_time, start_time, easing)
    Object.elements.append(animation)
    return animation.current