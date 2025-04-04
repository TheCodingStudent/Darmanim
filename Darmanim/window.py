from __future__ import annotations
import os
import pygame
import subprocess
from Darmanim.time import Clock
from Darmanim.color import get_color
from Darmanim.values import Object, Action, get_value, LerpEventGroup


class VideoMP4:
    def __init__(self, output: str, surface: pygame.Surface):
        self.output = output
        self.surface = surface
        self.width, self.height = self.surface.get_size()
        self.frame_count = 0
        self.folder = os.path.join(os.path.dirname(__file__), 'frames')

    def write(self) -> None:
        pygame.image.save(self.surface, f'{self.folder}/screen_{self.frame_count:05d}.png')
        self.frame_count += 1
    
    def clean_folder(self) -> None:
        for file in os.listdir(self.folder):
            os.remove(f'{self.folder}/{file}')

    def release(self) -> None:
        command = [
            'ffmpeg',
            '-r', str(Clock.fps),
            '-f', 'image2',
            '-s', f'{self.width}x{self.height}',
            '-i', f'{self.folder}/screen_%05d.png',
            '-pix_fmt', 'yuv420p',
            '-vcodec', 'libx264',
            '-crf', '25',
            self.output
        ]
        
        subprocess.run(command, check=True)
        self.clean_folder()


class Surface:
    def __init__(
        self,
        x: int, y: int,
        size: tuple[int, int]=(0, 0), flags: int=0,
        color: any='background', border: any='white', border_width: int=0
    ):
        if size == (0, 0) and flags == 0: flags = pygame.FULLSCREEN
        self.screen = pygame.Surface(size, flags)
        self.color = get_color(color)
        self.border = get_color(border)
        self.border_width = get_value(border_width)
        self.width, self.height = self.screen.get_size()

        self.elements = []
        self.hidden = []

        self.rect = self.screen.get_rect(topleft=(x, y))
    
    def displace_to(self, x: int, y: int, start_time: float=0, transition_time: float=0) -> Surface:
        if start_time == 0:
            if transition_time == 0: self.rect.topleft = (x, y)
            else: LerpEventGroup(
                (self.rect, self.rect),
                ('x', 'y'), (self.rect.x, self.rect.y), (x, y),
                transition_time
            )
        else:
            Action(self.displace_to, start_time, args=(x, y, 0, transition_time))

        return self

    def hide(self, element: any, start_time: float, keep_updating: bool=False) -> Surface:
        if start_time == 0:
            self.elements.remove(element)
            self.hidden.append((element, keep_updating))
            return self
        
        Action(self.hide, start_time, args=(element, 0))
        return self
    
    def unhide(self, element: any, start_time: float) -> Surface:
        if start_time == 0:
            self.elements.append(element)
            for hidden, update in self.hidden:
                if hidden == element: self.hidden.remove((element, update))
            return self
    
        Action(self.unhide, start_time, args=(element, 0))
        return self

    def remove(self, element: any, start_time: float) -> Surface:
        if start_time == 0:
            self.elements.remove(element)
            return self
        
        Action(self.remove, start_time, args=(element, 0))
        return self
    
    def add(self, element: any, x: int|None=None, y: int|None=None, start_time: float=0) -> any:
        if start_time != 0:
            Action(self.add, start_time, args=(element, x, y))
            return element

        self.elements.append(element)
        if hasattr(element, 'attach'):
            try: element.attach(self, x, y)
            except TypeError: element.attach(self)

        return element
    
    def attach(self, window: Window) -> None:
        self.window = window

    def show(self) -> None:
        self.screen.fill(self.color.rgb())
        for element in self.elements: element.show()
        if self.border_width > 0:
            pygame.draw.rect(self.screen, self.border.rgb(), (0, 0, self.width, self.height), width=self.border_width.get(int))
        self.window.screen.blit(self.screen, self.rect)
    
    def add_element(self, element: any, z_index: int) -> None:
        element.z_index = z_index
        self.elements.append(element)
        self.elements = sorted(self.elements, key=lambda e: e.z_index, reverse=True)
    
    def update(self) -> None:
        for element in self.elements:
            if hasattr(element, 'update'):
                try: element.update(True)
                except TypeError: element.update()
        
        for element, update in self.hidden:
            if not update: continue
            if hasattr(element, 'update'):
                try: element.update(True)
                except TypeError: element.update()


class Window(Surface):
    def __init__(
        self, size: tuple[int, int]=(0, 0), flags: int=0,
        title: str='Darmanim', icon: str='ratoncita.png',
        color: any='background',
        output: str='', record_time: float=0, fps: int=60
    ):
        super().__init__(0, 0, size, flags, color)
        pygame.init()
        Clock.fps = fps
        self.screen = pygame.display.set_mode(size, flags)

        self.output = output
        self.record_time = record_time
        self.recording = False

        self.font = pygame.font.SysFont('Arial', 32)

        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

    def record(self) -> None:
        self.recording = True
        self.video = VideoMP4(self.output, self.screen)

    def show(self) -> None:
        self.screen.fill(self.color.rgb())
        for element in self.elements:
            element.show()

    def update(self) -> None:
        Clock.tick()
        Object.update_all()
        super().update()

    def run(self) -> None:
        self.running = True
        
        Clock.time = -1
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
            
            self.update()
            self.show()

            if self.recording and Clock.time >= 0:
                self.video.write()
                self.running = not (self.record_time != 0 and Clock.time >= self.record_time + Clock.dt)
                text = self.font.render(f'{self.video.frame_count}/{Clock.fps * self.record_time}', True, 'white')
                self.screen.blit(text, (10, 10))
        
            pygame.display.update()

        pygame.quit()
        if self.recording: self.video.release()