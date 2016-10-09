#     A game developed with Python based on physics concepts.
#     Copyright (C) 2014 - Author: Rubens Pessoa de Barros Filho
# 
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License along
#     with this program; if not, write to the Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import random
import math
from Physics.Particle import Particle
from Physics.Spring import Spring
from Physics.Util import collide, lennard_jones


class Environment:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.springs = []
        self.particle_functions1 = []
        self.particle_functions2 = []
        self.function_dict = {
            'move': (1, lambda p: p.move()),
            'drag': (1, lambda p: p.experience_drag()),
            'bounce': (1, lambda p: self.bounce(p)),
            'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
            'collide': (2, lambda p1, p2: collide(p1, p2)),
            'lennard_jones': (2, lambda p1, p2: lennard_jones(p1, p2))
        }

        self.colour = (255, 255, 255)
        self.mass_of_water = 0
        self.mass_of_air = 0.02
        self.elasticity = 0.75
        self.acceleration = (0, 0)

    def add_particles(self, n=1, **kargs):
        for i in range(n):
            size = kargs.get('size', random.randint(30, 50))
            #size = 20
            #mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            p = Particle(x, y, size)
            p.speed = kargs.get('speed', random.random())
            p.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            p.colour = kargs.get('colour', (0, 0, 0))

            # Set self.mass_of_... according with the environment you want to simulate.

            p.drag = (p.mass / (p.mass + self.mass_of_water)) ** p.size

            self.particles.append(p)

    def add_springs(self, p1, p2, length=50, strength=0.5):
        self.springs.append(Spring(self.particles[p1], self.particles[p2], length, strength))

    def add_functions(self, function_list):

        for func in function_list:
            (n, f) = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print ("No such function: %s" % f)

    def update(self):
        for i, particle in enumerate(self.particles):
            for f in self.particle_functions1:
                f(particle)
            for particle2 in self.particles[i + 1:]:
                for f in self.particle_functions2:
                    f(particle, particle2)

        for spring in self.springs:
            spring.update()

    def bounce(self, particle):
        # Para condicoes Periodicas de Contorno:
        #
        # if particle.x > self.width - particle.size:
        #     particle.x = particle.size
        #     particle.angle = particle.angle
        #
        # elif particle.x < particle.size:
        #     particle.x = self.width - particle.size
        #     particle.angle = particle.angle
        #
        # if particle.y > self.height - particle.size:
        #     particle.y = particle.size
        #     particle.angle = particle.angle
        #
        # elif particle.y < particle.size:
        #     particle.y = self.height - particle.size
        #     particle.angle = particle.angle
        #

        if particle.x > self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= particle.elasticity

        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

    def find_particle(self, x, y):
        for p in self.particles:
            if math.hypot(p.x - x, p.y - y) <= p.size:
                return p
        return None

