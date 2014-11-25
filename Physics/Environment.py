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
from Physics.Util import collide, elasticity

class Environment:
    
    def __init__(self, (width, height)):
        self.width = width
        self.height = height
        self.particles = []
        
        self.colour = (255,255,255)
        self.mass_of_air = 0.02
        self.elasticity = elasticity
        
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
    
    def update(self):
        for i, particle in enumerate(self.particles):
            particle.move()
            self.bounce(particle)
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)
    
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