from __future__ import annotations
from Darmanim.time import Clock


class Object:
    elements: list = []

    def __init__(self, start_time: float=0):
        self.time = 0
        self.start_time = start_time
        Object.add(self)

    def update_time(self) -> None:
        if Clock.time < self.start_time: return
        self.time += Clock.get_fps()

    def add(element: any) -> None:
        Object.elements.append(element)
    
    def update_all() -> None:
        for element in Object.elements:
            element.update_time()
            if element.update():
                Object.elements.remove(element)


class Event(Object):
    def __init__(self, element: any, attribute: str, value: any, start_time: float=0, transition_time: float=0, update_element: bool=False):
        super().__init__(start_time)
        self.element = element
        self.attribute = attribute
        self.value = get_value(value)
        self.transition_time = transition_time
        self.update_element = update_element
        Object.add(self)

    def update(self) -> bool:
        if Clock.time < self.start_time: return False

        setattr(self.element, self.attribute, self.value.get())
        if self.update_element: self.element.update()

        if self.transition_time == 0: return True

        return False
    

class LerpEvent(Object):
    def __init__(self, element: any, attribute: str, start: any, end: any, transition_time: float, start_time: float=0, update_element: bool=False):
        super().__init__(start_time)
        self.element = element
        self.attribute = attribute
        self.start = get_value(start)
        self.end = get_value(end)
        self.transition_time = transition_time
        self.update_element = update_element
        Object.add(self)

    def update(self) -> bool:
        if Clock.time < self.start_time: return False
        if self.time >= self.transition_time:
            setattr(self.element, self.attribute, self.end.get())
            return True

        t = self.time / self.transition_time
        value = self.start + (self.end - self.start) * t
        setattr(self.element, self.attribute, value)
        if self.update_element: self.element.update()

        return False


class LerpEventGroup(Object):
    def __init__(self, elements: tuple[any], attributes: tuple[str], starts: tuple[any], ends: tuple[any], transition_time: float, start_time: float=0, update_elements: bool=False):
        super().__init__(start_time)
        self.elements = elements
        self.attributes = attributes
        self.starts = get_values(starts)
        self.ends = get_values(ends)
        self.transition_time = transition_time
        self.update_elements = update_elements
        Object.add(self)

    def update(self) -> bool:
        if Clock.time < self.start_time: return False
        if self.time >= self.transition_time:
            for element, attribute, end in zip(self.elements, self.attributes, self.ends):
                setattr(element, attribute, end.get())
            return True

        t = self.time / self.transition_time
        for element, attribute, start, end in zip(self.elements, self.attributes, self.starts, self.ends):
            value = start + (end - start) * t
            setattr(element, attribute, value)
            if self.update_elements: element.update()

        return False


class Action(Object):
    def __init__(self, action: callable, start_time: float, args: tuple[any]=(), kwargs: dict[str, any]={}):
        super().__init__(start_time)

        self.action = action
        self.args = args
        self.kwargs = kwargs
    
    def update(self) -> bool:
        if Clock.time < self.start_time: return False
        self.action(*self.args, **self.kwargs)
        return True


class ActionEvent(Object):
    def __init__(self, action: callable, start_time: float, transition_time: float, args: tuple[any]=(), kwargs: dict[str, any]={}):
        super().__init__(start_time)

        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.transition_time = transition_time
    
    def update(self) -> bool:
        if Clock.time < self.start_time: return False
        self.action(*self.args, **self.kwargs)
        return self.time >= self.transition_time


def get_value(value: any) -> Value:
    if isinstance(value, (Value, LerpValue, ContinuosValue)): return value
    return Value(value)


def get_values(values: list[any]) -> list[Value]:
    return [get_value(value) for value in values]


class Value:
    def __init__(self, value: any):
        self.value = value
    
    def get(self, cast: type|None=None) -> any:
        if cast is None: return self.value
        return cast(self.value)
    
    def lerp(self, other: Value, t: float) -> any:
        return self.value + (other.value - self.value) * t

    def __neg__(self) -> Value:
        return Value(-self.value)

    def __mul__(self, other: any) -> any:
        return self.value * other
    
    def __rmul__(self, other: any) -> any:
        return self.value * other
    
    def __add__(self, other: any) -> any:
        return self.value + other

    def __radd__(self, other: any) -> any:
        return self.value + other
    
    def __sub__(self, other: any) -> any:
        return self.value - other
    
    def __rsub__(self, other: any) -> any:
        return other - self.value

    def __truediv__(self, other: any) -> any:
        return self.value / other
    
    def __rtruediv__(self, other: any) -> any:
        return other / self.value
    
    def __eq__(self, other: any) -> any:
        return self.value == other

    def __index__(self) -> int:
        return int(self.value)
    
    def __repr__(self) -> str:
        return f'Value({self.value})'


class LerpValue(Object, Value):
    def __init__(self, start: float, end: float, transition_time: float, start_time: float=0, function: callable=None):
        Object.__init__(self, start_time)
        Value.__init__(self, start)

        self.t = 0
        self.end = end
        self.function = function
        self.value = self.start = start
        if function is not None: self.value = function(self.value)
        self.transition_time = transition_time
    
    def update(self) -> bool:
        if Clock.time < self.start_time: return False

        self.t = min(self.time/self.transition_time, 1)
        self.value = self.start + (self.end - self.start) * self.t
        if self.function: self.value = self.function(self.value)

        return self.t == 1
    
    def __neg__(self) -> LerpValue:
        return LerpValue(-self.start, -self.end, self.transition_time)


class SequenceValue(Object, Value):
    def __init__(
        self, values: list[any],
        transition_time: float, start_time: float=0,
        function: callable=None,
        wrap: bool=False
    ):
        Object.__init__(self, start_time)
        Value.__init__(self, values[0])
        self.values = list(values)
        if wrap: self.values.append(self.values[0])
        self.function = function
        self.transition_time = transition_time
        self.lerp_transition_time = transition_time / (len(self.values) - 1)
        self.current_lerp = None

    def get_next_lerp(self) -> LerpValue|None:
        if len(self.values) == 1: return None
        start = self.values.pop(0)
        return LerpValue(start, self.values[0], self.lerp_transition_time)

    def update(self) -> bool:
        if self.current_lerp is None or self.current_lerp.t == 1:
            self.current_lerp = self.get_next_lerp()
            if self.current_lerp is None: return True
        self.value = self.current_lerp.get()

        return False


class ContinuosValue(Object, Value):
    def __init__(self, start: float, step: float, transition_time: float, start_time: float=0, function: callable=None):
        Object.__init__(self, start_time)
        Value.__init__(self, start)

        self.t = 0
        self.step = step
        self.value = self.start = start
        if function is not None: self.value = function(self.value)
        self.function = function
        self.transition_time = transition_time
    
    def update(self) -> False:
        self.t = self.time / self.transition_time
        self.value = self.start + self.step * self.t
        if self.function: self.value = self.function(self.value)
        return False

    def __neg__(self) -> LerpValue:
        return ContinuosValue(-self.start, -self.step, self.transition_time)