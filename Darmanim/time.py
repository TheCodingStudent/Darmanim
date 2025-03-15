import pygame

type time = float|str


class Clock:
    dt: float = 0
    fps: int = 60
    time: float = -1
    clock = pygame.time.Clock()
    
    def tick() -> None:
        Clock.clock.tick(Clock.fps)

        Clock.dt = 1 / Clock.fps
        if Clock.time == -1: Clock.dt = Clock.time = 0
        else: Clock.time += Clock.dt

    def get_fps() -> float:
        return Clock.fps
    
    def get_real_fps() -> float:
        return Clock.clock.get_fps()