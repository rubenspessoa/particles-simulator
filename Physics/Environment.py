'''
Created on 25/11/2014

@author: rubenspessoa
'''
import random, math
from Physics.Particle import Particle
from Physics.Util import *

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
            size = kargs.get('size', random.randint(10,20))
            mass = kargs.get('mass', random.randint(100,10000))
            
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))
            
            p = Particle((x, y), size, mass)
            p.speed = kargs.get('speed', random.random())
            p.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            p.colour = kargs.get('colour', (0,0,255))
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
        
            
            
            
        
        