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

import random, math
from Physics.Particle import Particle
from Physics.Spring import Spring
from Physics.Util import addVectors

class Environment:
    
    def __init__(self, (width, height)):
        self.width = width
        self.height = height
        self.particles = []
        self.springs = []
        self.particle_functions1 = []
        self.particle_functions2 = []
        self.function_dict = {
            'move': (1, lambda p: p.move()),
            'drag': (1, lambda p: p.experienceDrag()),
            'bounce': (1, lambda p: self.bounce(p)),
            'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
            'collide': (2, lambda p1, p2: self.collide(p1, p2))
        }
        
        self.colour = (255,255,255)
        self.mass_of_air = 0.02
        self.elasticity = 0.75
        self.acceleration = (0,0)
        
    def addParticles(self, n=1, **kargs):
        for i in range(n):
            size = kargs.get('size', random.randint(30,50))
            mass = kargs.get('mass', random.randint(100,10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))
            
            p = Particle((x, y), size, mass)
            p.speed = kargs.get('speed', random.random())
            p.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            p.colour = kargs.get('colour', (0,0,0))
            p.drag = (p.mass/(p.mass + self.mass_of_air)) ** p.size
            
            self.particles.append(p)
    
    def addSprings(self, p1, p2, length=50, strength=0.5):
        self.springs.append(Spring(self.particles[p1], self.particles[p2], length, strength))
        
    def addFunctions(self, function_list):
        
        for func in function_list:
            (n, f) = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print "No such function: %s" % f
        
    def update(self):
        for i, particle in enumerate(self.particles):
            for f in self.particle_functions1:
                f(particle)
            for particle2 in self.particles[i+1:]:
                for f in self.particle_functions2:
                    f(particle, particle2)
        for spring in self.springs:
            spring.update()
    
    def bounce(self, particle):
        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= particle.elasticity

        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity
            
    def findParticle(self, x, y):
        for p in self.particles:
            if math.hypot(p.x - x, p.y - y) <= p.size:
                return p
        return None
    
    def collide(self, p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        distance = math.hypot(dx, dy)
        
        if distance < p1.size + p2.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi
            total_mass = p1.mass + p2.mass
            
            (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed * (p1.mass - p2.mass)/total_mass), 
                                              (angle, 2*p2.speed*p2.mass/total_mass))
            (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed * (p2.mass - p1.mass)/total_mass), 
                                              (angle + math.pi, 2*p1.speed*p1.mass/total_mass))
            
            elasticity = p1.elasticity * p2.elasticity
            p1.speed *= elasticity
            p2.speed *= elasticity
            
            overlap = 0.5 * (p1.size + p2.size - distance + 1)
            p1.x += math.sin(angle)*overlap
            p1.y -= math.cos(angle)*overlap
            p2.x -= math.sin(angle)*overlap
            p2.y += math.cos(angle)*overlap