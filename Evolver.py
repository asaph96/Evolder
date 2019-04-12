from p5 import Vector, random_uniform, remap
from math import pi
import pygame as pg


class Evolver:
    mutation_rate = 0.1
    radius = 5
    maxspeed = 5
    maxforce = 0.5
    clone_rate = 0.02

    def __init__(self, x, y, dna=False):

        self.pos = Vector(x, y)
        self.acc = Vector(0, 0)
        self.vel = Vector(0, -2)
        self.__health = 1

        if not dna:
            self.dna = []
            for _ in range(4):
                self.dna.append(random_uniform(-2, 2))
        else:
            self.dna = []
            for gene in dna:
                if random_uniform(1) < self.mutation_rate:
                    self.dna.append((gene + random_uniform(-1, 1))/2)
                else:
                    self.dna.append(gene)

    @property
    def _pos(self):
        return (self.pos.x, self.pos.y,)

    @property
    def health(self):
        if self.__health > 0:
            return self.__health
        else:
            return 0
    @health.setter
    def health(self, health):
        if health >= 1:
            self.__health = 1
        else:
            self.__health = health

    def seek(self, target):
        desired = target - self.pos
        desired.magnitude = self.maxspeed
        steer = desired - self.vel
        steer.limit(self.maxforce)
        return steer

    def eat(self, matrix, nutrition, perception):
        record = 10**10
        closest = None
        for element in reversed(matrix):
            distance = self.pos.dist(element)
            if distance < self.radius * 2:
                matrix.remove(element)
                self.health += nutrition
            elif distance < record and distance < perception:
                record = distance
                closest = element

        if closest != None:
            return self.seek(closest)
        return Vector(0, 0)

    def update(self):
        self.health -= 0.005
        # print(self.vel, "antes")
        self.vel += self.acc
        # print(self.vel, "depois")
        self.vel.limit(self.maxspeed)
        self.pos += self.vel
        self.acc *= 0

    def applyForce(self, force):
        self.acc += force

    def behaviour(self, good, bad):
        steerG = self.eat(good, 0.2, remap(self.dna[2], (-2, 2), (5, 100)))
        steerB = self.eat(bad, -1, remap(self.dna[3], (-2, 2), (5, 100)))

        steerG *= self.dna[0]
        steerB *= self.dna[1]

        self.applyForce(steerG)
        self.applyForce(steerB)

# region p5_display
    # def display(self, debug=False):

    #     gr = color(0, 255, 0)
    #     rd = color(255, 0, 0)
    #     col = lerpColor(rd, gr, self.health)

    #     angle = self.vel.heading() + PI/2

    #     pushMatrix()
    #     translate(self.pos.x, self.pos.y)
    #     rotate(angle)

    #     if debug:
    #         dna2 = map(self.dna[2],-2,2,5,100)
    #         dna3 = map(self.dna[3],-2,2,5,100)
    #         strokeWeight(3)
    #         stroke(0, 255, 0)
    #         noFill()
    #         line(0, 0, 0, -self.dna[0] * 25)
    #         strokeWeight(2)
    #         ellipse(0, 0, dna2 * 2, dna2 * 2)
    #         stroke(255, 0, 0)
    #         line(0, 0, 0, -self.dna[1] * 25)
    #         ellipse(0, 0, dna3 * 2, dna3 * 2)

    #     fill(col)
    #     stroke(255)
    #     strokeWeight(1)

    #     beginShape()
    #     vertex(0, -self.radius *2)
    #     vertex(-self.radius, self.radius *2)
    #     vertex(self.radius, self.radius *2)
    #     endShape(CLOSE)

    #     popMatrix()
# endregion

    def display(self, window, debug=False):
        gr = Vector(0, 255, 0)
        rd = Vector(255, 0, 0)
        col = tuple([int(i) for i in rd.lerp(gr, self.health)])
        # print(col)
        pg.draw.circle(window, col, self._pos, self.radius*2)

        angle = self.vel.angle + pi/2
        pg.transform.rotate(window, angle)

        if debug:
            dna2 = remap(self.dna[2], (-2, 2), (5, 100))
            dna3 = remap(self.dna[3], (-2, 2), (5, 100))
            lineg = tuple(self.pos * dna2)
            liner = tuple(self.pos * dna3)

            pg.draw.aaline(window, tuple(gr), self._pos,
                           (lineg[:2]))
            pg.draw.aaline(window, tuple(rd), self._pos,
                           (liner[:2]))

    def boundaries(self, w, h):
        d = 50
        desired = None

        if self.pos.x < d:
            desired = Vector(self.maxspeed, self.vel.y)
        elif self.pos.x > (w - d):
            desired = Vector(-self.maxspeed, self.vel.y)

        if self.pos.y < d:
            desired = Vector(self.vel.x, self.maxspeed)
        elif self.pos.y > (h - d):
            desired = Vector(self.vel.x, -self.maxspeed)

        if desired:
            desired.normalize()
            desired *= self.maxspeed
            steer = desired - self.vel
            steer.limit(self.maxforce)
            self.applyForce(steer)

    def dead(self):
        return self.health <= 0

    def clone(self, w, h):
        if random_uniform(1) < self.clone_rate and self.health > 0.9:
            x = random_uniform(w)
            y = random_uniform(h)
            print("Hey, cloned")
            return Evolver(x, y, self.dna)
        else:
            return False
