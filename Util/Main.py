'''
Created on 18/11/2014

@author: rubenspessoa
'''

if __name__ == "__main__":
    import random, math, pygame
    from Models import Particle 
        
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
        particle.speed = random.random()
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
            particle.display(screen)
        
        pygame.display.flip()