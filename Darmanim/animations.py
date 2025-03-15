from __future__ import annotations
import numpy as np
from Darmanim.globals import LerpValue


def draw(animation_time: int=1, default: any=0):
    def inner_draw(func: callable):
        i = LerpValue(0, 1, animation_time)
        def wrapper(x: np.array, *args, **kwargs):
            y = func(x, *args, **kwargs)
            y[int(i * len(x)):] = default
            return y
        return wrapper
    return inner_draw


def squeeze(animation_time: int=1, from_: float=0, to: float=1):
    def inner_draw(func: callable):
        i = LerpValue(from_, to, animation_time)
        def wrapper(x: np.array, *args, **kwargs):
            y = func(x, *args, **kwargs)
            return y * i
        return wrapper
    return inner_draw