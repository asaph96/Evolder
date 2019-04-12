import pygame as pg
from p5 import random_uniform as rd
from p5 import Vector
from Evolver import *

pg.init()

w, h = 800, 600

window = pg.display.set_mode((w, h))
pg.display.set_caption("APH")

evolvers = [Evolver(rd(w), rd(h)) for _ in range(10)]
food = [Vector(rd(w), rd(h)) for _ in range(100)]
poison = [Vector(rd(w), rd(h)) for _ in range(30)]


run = True
while run:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    window.fill(0)

    if rd(1) < 0.3:
        food.append(Vector(rd(w), rd(h)))
    if rd(1) < 0.1:
        poison.append(Vector(rd(w), rd(h)))

    for f in food:
        pg.draw.circle(window, (0, 255, 0), (f.x, f.y), 2)
    for p in poison:
        pg.draw.circle(window, (255, 0, 0), (p.x, p.y), 2)

    for e in reversed(evolvers):
        e.boundaries(w, h)
        e.behaviour(food, poison)
        e.update()
        e.display(window)

        if e.dead():
            evolvers.remove(e)

        son = e.clone(rd(w), rd(h))
        if son:
            evolvers.append(son)

    pg.display.update()

pg.quit()
