import math
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1000, 1000))
WIDTH, HEIGHT = SCREEN.get_size()
RUNNING = True


def azimut(vector: tuple[float, float]) -> float:
    return math.atan2(-vector[1], vector[0])


a = (500, 100)
b = (900, 500)
r = 400

m = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
t = b[0] - a[0], b[1] - a[1]
n = b[1] - a[1], a[0] - b[0]
dn = math.hypot(*n)
d = math.hypot(*t)

h = math.sqrt(r*r - d*d/4)
reverse = True


if not reverse: o = m[0] + h*n[0]/dn, m[1] + h*n[1]/dn
else: o = m[0] - h*n[0]/dn, m[1] - h*n[1]/dn

flip = True
av = a[0] - o[0], a[1] - o[1]
bv = b[0] - o[0], b[1] - o[1]

if flip: av, bv = bv, av

rect = (o[0] - r, o[1] - r, 2*r, 2*r)

while RUNNING:
    SCREEN.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    
    pygame.draw.circle(SCREEN, 'white', a, 3)
    pygame.draw.circle(SCREEN, 'white', b, 3)
    pygame.draw.line(SCREEN, 'darkgray', a, b)
    pygame.draw.circle(SCREEN, 'red', m, 3)
    pygame.draw.circle(SCREEN, 'white', o, 3)
    pygame.draw.line(SCREEN, 'darkgray', m, o)

    pygame.draw.circle(SCREEN, 'blue', o, r, width=1)

    pygame.draw.arc(SCREEN, 'white', rect, azimut(av), azimut(bv), width=1)

    pygame.display.update()