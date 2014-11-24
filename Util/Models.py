'''
Created on 18/11/2014

@author: rubenspessoa
'''

import pygame, math
from Util.Main import addVectors
from twisted.conch.test.test_helper import WIDTH

class Particle():
    def __init__(self, (x, y), size):
        
        self.x          = x
        self.y          = y
        self.size       = size
        self.color      = (0,0,255)
        self.thickness  = 1
        self.speed      = 0
        self.angle      = 0

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
    
    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
        
    def bounce(self, width, height):
        
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
    
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
    
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
    
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle