import os
import pygame
import subprocess
from Darmanim.time import Clock
from Darmanim.globals import Object
from Darmanim.color import get_color


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


class Window:
    def __init__(
        self, size: tuple[int, int]=(0, 0), flags: int=0,
        title: str='Darmanim', icon: str='ratoncita.png',
        color: any='background',
        output: str='', record_time: float=0, fps: int=60
    ):
        pygame.init()
        Clock.fps = fps

        if size == (0, 0) and flags == 0: flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        self.color = get_color(color)
        self.elements = []
        self.functions = []

        self.width, self.height = self.screen.get_size()

        self.output = output
        self.record_time = record_time
        if output != '': self.video = VideoMP4(output, self.screen)
        else: self.video = None
        self.recording = False

        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

    def record(self) -> None:
        self.recording = True

    def add(self, element: any, x: int|None=None, y: int|None=None) -> None:
        self.elements.append(element)
        if hasattr(element, 'attach'):
            try: element.attach(self, x, y)
            except TypeError: element.attach(self)
        return element

    def show(self) -> None:
        for element in self.elements:
            element.show()

    def update(self) -> None:
        Clock.tick()
        Object.update_all()

        for element in self.elements:
            if hasattr(element, 'update'):
                element.update(True)

    def run(self) -> None:
        self.running = True
        
        Clock.time = -1
        while self.running:
            self.screen.fill(self.color.rgb())
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
            
            self.update()
            self.show()
            pygame.display.update()

            if self.recording and self.output and Clock.time >= 0:
                self.video.write()
                self.running = not (self.record_time != 0 and Clock.time >= self.record_time + Clock.dt)
        
        pygame.quit()
        if self.recording and self.video: self.video.release()