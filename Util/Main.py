'''
Created on 18/11/2014

@author: rubenspessoa
'''
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
        #self.speed *= drag
        
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
            
def addVectors((angle1, length1), (angle2, length2)):
        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        angle = 0.5 * math.pi - math.atan2(y, x)
        length  = math.hypot(x, y)
        return (angle, length)
    
if __name__ == "__main__":
    import random, math, pygame
    from Models import Particle 
    
    elasticity = 0.75
    gravity = (math.pi, 0.002)
    
    (width, height) = (800, 600)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Physics One')
    number_of_particles = 10
    my_particles = []

    for i in range(number_of_particles):
        size = random.randint(10,20)
        x = random.randint(size, width - size)
        y = random.randint(size, height - size)
        particle = Particle((x, y), size)
        particle.speed = 15
        particle.angle = random.uniform(0, math.pi*2)
        my_particles.append(particle)
        
    #-# LOOP PRINCIPAL #-#
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255,255,255))

        for particle in my_particles:
            particle.move()
            particle.bounce(width, height)
            particle.display(screen)
        
        pygame.display.flip()