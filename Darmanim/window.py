import cv2
import pygame
import numpy as np
from typing import Generator
from Darmanim.time import Clock
from Darmanim.globals import Object
from Darmanim.color import Color, get_color


class Video:
    def __init__(self, output: str, width: int, height: int):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(output, fourcc, Clock.fps, (width, height), True)
    
    def write(self, screen: pygame.Surface) -> Generator:
        frame = self.pg_to_cv2(screen)
        self.video.write(frame)

    def pg_to_cv2(self, screen: pygame.Surface) -> np.ndarray:
        cvarray = pygame.surfarray.array3d(screen)
        cvarray = cvarray.swapaxes(0, 1)
        cvarray = cv2.cvtColor(cvarray, cv2.COLOR_RGB2BGR)
        return cvarray
    
    def release(self) -> None:
        self.video.release()


class Window:
    def __init__(self, size: tuple[int, int]=(0, 0), flags: int=0, title: str='Darmanim', icon: str='ratoncita.png', color: Color=Color.black, output: str=''):
        pygame.init()


        # PROPERTIES
        if size == (0, 0) and flags == 0: flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        self.color = get_color(color)
        self.elements = []

        self.width, self.height = self.screen.get_size()

        # VIDEO WRITER
        self.output = output
        if output != '': self.video = Video(output, self.width, self.height)
        else: self.video = None

        # SETUP
        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

        Clock.tick()

    def add(self, element: any, x: int|None=None, y: int|None=None) -> None:
        self.elements.append(element)
        if hasattr(element, 'attach'): element.attach(self, x, y)

    def show(self) -> None:
        for element in self.elements:
            element.show()

    def update(self) -> None:
        Clock.tick()
        Object.update_all()

    def run(self) -> None:
        self.running = True
        Clock.time = 0
        while self.running:
            self.screen.fill(self.color.rgb())
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
            
            self.update()
            self.show()
            pygame.display.update()

            if self.output: self.video.write(self.screen)
        
        if self.video: self.video.release()