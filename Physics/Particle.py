'''
Created on 25/11/2014

@author: rubenspessoa
'''

from Physics.Util import *
import math

gravity = (math.pi, 0.02)

class Particle():
    def __init__(self, (x, y), size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9

    def move(self):
        # Gravidade 
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag
    
    def mouseMove(self, (x, y)):
        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5 * math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1
        