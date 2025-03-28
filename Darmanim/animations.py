from __future__ import annotations
import numpy as np
from Darmanim.globals import LerpValue


def draw(animation_time: float=1, start_time: float=0, default: any=0):
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