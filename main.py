import pygame
from pygame.locals import *
import math


class Obstacle:

    def __init__(self, pos, dims):
        self.pos = pos
        self.dims = dims
        self.figure = None
        self.color = (255, 0, 0)

    def draw(self):
        self.figure = pygame.draw.rect(screen, self.color, self.pos + self.dims)


class Electron:

    def __init__(self, pos, vel):
        self.charge = -1
        self.mass = 1
        self.pos = [pos.copy()]
        self.current_pos = pos.copy()
        self.figure = None
        self.status = True
        self.active = 0
        self.vel = vel.copy()

    def draw(self):
        self.figure = pygame.draw.circle(screen, (0, 255, 255), self.current_pos, 5)

    def move(self, force):
        pos = self.current_pos.copy()
        self.vel[0] += force[0]
        self.vel[1] += force[1]
        pos[0] += self.vel[0]
        pos[1] += self.vel[1]
        self.pos.append(pos)

    def update_pos(self):
        self.current_pos = self.pos[-1].copy()
        self.pos.pop(0)


screen = pygame.display.set_mode((1200, 600))


obstacles = [
    Obstacle([600, 0], [10, 250]),
    Obstacle([600, 350], [10, 250]),
    Obstacle([600, 280], [10, 40]),
    Obstacle([1180, 0], [20, 600])
]

electrons = [Electron([500, y], [4, 0]) for y in range(0, 600, 3)]

hyp_calc = lambda vector1, vector2: math.sqrt((vector1[0] - vector2[0]) ** 2 + (vector1[1] - vector2[1]) ** 2)


def angle_calc(vector1, vector2):
    return math.asin((vector1[1] - vector2[1]) / hyp_calc(vector1, vector2))


def force(electron):
    k = 2
    output = [0, 0]
    for e in electrons:
        if e is not electron:
            mag = k / (hyp_calc(e.current_pos, electron.current_pos)**2)
            dir = angle_calc(e.current_pos, electron.current_pos)
            if e.current_pos[0] > electron.current_pos[0]:
                output[0] -= abs(math.cos(dir) * mag)
            else:
                output[0] += abs(math.cos(dir) * mag)
            if e.current_pos[1] > electron.current_pos[1]:
                output[1] -= abs(math.sin(dir) * mag)
            else:
                output[1] += abs(math.sin(dir) * mag)
    return output


i = 0

def force_thread():
    global electrons
    for e in electrons:
        if e.status:
            if e.status:
                e.move(force(e))

while True:

    screen.fill((0, 0, 0))

    for o in obstacles:
        o.draw()

    for e in electrons:
        e.draw()
        for o in obstacles:
            if o.pos[0] <= e.current_pos[0] <= o.pos[0] + o.dims[0] and (o.pos[1] <= e.current_pos[1] <= o.pos[1] + o.dims[1]): # or o.pos[1] <= e.current_pos[1] <= o.pos[1] + o.dims[1]):
                e.status = False
        if e.status:
            e.move(force(e))

    for e in electrons:
        if e.status:
            e.update_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    pygame.display.update()

    # if i % 1 == 0:
    # electrons.append(Electron([0, 300], [random.randint(0, 5) * random.random(), random.randint(-5, 5) * random.random()]))

    i += 1
