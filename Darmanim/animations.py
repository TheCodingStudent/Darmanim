from __future__ import annotations
import numpy as np
from Darmanim.values import LerpValue, ContinuosValue


def draw(animation_time: float, start_time: float=0, default: any=0):
    def inner_draw(func: callable):
        i = LerpValue(0, 1, animation_time, start_time)
        def wrapper(x: np.array, *args, **kwargs):
            y = func(x, *args, **kwargs)
            try:
                y[int(i * len(x)):] = default
                return y
            except TypeError:
                return y
        return wrapper
    return inner_draw


def phase(start: float, end: float, animation_time: float, start_time: float=0):
    def inner_phase(func: callable):
        value = LerpValue(start, end, animation_time, start_time)
        def wrapper(x: np.array, *args, **kwargs):
            return func(x + value.get(), *args, **kwargs)
        return wrapper
    return inner_phase


def continous_phase(start: float, step: float, animation_time: float, start_time: float=0):
    def inner_phase(func: callable):
        value = ContinuosValue(start, step, animation_time, start_time)
        def wrapper(x: np.array, *args, **kwargs):
            return func(x + value.get(), *args, **kwargs)
        return wrapper
    return inner_phase