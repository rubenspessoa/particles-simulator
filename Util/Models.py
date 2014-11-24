'''
Created on 18/11/2014

@author: rubenspessoa
'''

import pygame, math

class Particle():
    def __init__(self, (x, y), size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0,0,255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
    
    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
