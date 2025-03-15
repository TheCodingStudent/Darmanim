from __future__ import annotations
from Darmanim.time import Clock


class Object:
    elements: list = []

    def __init__(self):
        self.start_time = max(0, Clock.time)
        self.keep_updating = True
        Object.add(self)

    def update_time(self) -> None:
        self.time = max(Clock.time - self.start_time, 0) + Clock.dt

    def add(element: any) -> None:
        Object.elements.append(element)
    
    def update_all() -> None:
        for element in Object.elements:
            element.update_time()
            if not element.keep_updating: continue
            if element.update(): Object.elements.remove(element)


def get_value(value: any) -> Value:
    if isinstance(value, (Value, LerpValue)): return value
    return Value(value)


class Value:
    def __init__(self, value: any):
        self.value = value
    
    def get(self, cast: type|None=None) -> any:
        if cast is None: return self.value
        return cast(self.value)

    def __mul__(self, other: any) -> any:
        return self.value * other
    
    def __rmul__(self, other: any) -> any:
        return self.value * other
    
    def __add__(self, other: any) -> any:
        return self.value + other

    def __radd__(self, other: any) -> any:
        return self.value + other

    def __truediv__(self, other: any) -> any:
        return self.value / other
    
    def __rtruediv__(self, other: any) -> any:
        return other / self.value
    
    def __index__(self) -> int:
        return int(self.value)


class LerpValue(Object, Value):
    def __init__(self, start: float, end: float, transition_time: float):
        Object.__init__(self)
        Value.__init__(self, start)
        self.end = end
        self.value = self.start = start
        self.transition_time = transition_time
    
    def update(self) -> bool:
        t = min(self.time/self.transition_time, 1)
        self.value = self.start + (self.end - self.start) * t
        return t == 1
    
    def __neg__(self) -> LerpValue:
        return LerpValue(-self.start, -self.end, self.transition_time)