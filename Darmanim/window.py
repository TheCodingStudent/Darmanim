import pygame
from functools import partial

from Darmanim.color import Color, get_color
from Darmanim.globals import Object, Event


FONT = pygame.font.SysFont('arial', 12)


class Window(Object):
    def __init__(self, size: tuple[int, int]=(0, 0), flags: int=0, fill: Color|str=None):
        super().__init__()

        if size == (0, 0) and not flags: flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(size)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()
        self.running = False
        
        if fill is not None: self.fill = get_color(fill)
        else: self.fill = Color()
        
        self.paused = False
        self.width, self.height = self.screen.get_size()
    
    def add(self, element: Object, time: str|int=0, **kwargs) -> None:
        # print(element)
        # if hasattr(element, 'copy'): element = element.copy()
        if time: return Event(function=element.attach, args=(self, ), event_time=time)
        return element.attach(self)
 
    def remove(self, element: Object, time: str|int=0, **kwargs) -> None:
        if time: return Event(function=Object.elements.remove, args=(element, ), event_time=time)
        return Object.elements.remove(element)
     
    def stop(self) -> None:
        self.running = False
    
    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.stop()
    
    def pause(self, time: str) -> None:
        Event(function=partial(setattr, self, 'paused'), args=(True, ), event_time=time)
    
    def update(self) -> None:
        self.surface.blit(FONT.render(str(Object.clock.time), True, 'white'), (0, 0))
        self.surface.blit(FONT.render(f'fps={Object.clock.get_fps()}', True, 'white'), (0, 20))
        if not self.paused: Object._update_all()
    
    def clear(self) -> None:
        self.screen.fill('black')
        self.surface.fill(self.fill.rgba())

    def start(self) -> None:
        self.running = True
        while self.running:
            self.clear()
            self.events()
            self.update()
            self.screen.blit(self.surface, (0, 0))
            pygame.display.update()
        
        self.running = False