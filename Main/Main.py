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

from Physics.Environment import Environment
import pygame
import math

(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics One')
env = Environment((width, height))
env.add_functions(['move', 'accelerate', 'bounce', 'drag', 'collide'])
env.acceleration = (math.pi, 0.02)
env.add_particles(10)

env.add_springs(0, 1, length=200, strength=10)
env.add_springs(1, 2, length=200, strength=10)
env.add_springs(1, 4, length=200, strength=10)
env.add_springs(2, 0, length=200, strength=10)
env.add_springs(2, 4, length=200, strength=10)
env.add_springs(1, 3, length=200, strength=10)
env.add_springs(2, 3, length=200, strength=10)
env.add_springs(0, 3, length=200, strength=10)
env.add_springs(3, 4, length=200, strength=10)
env.add_springs(4, 0, length=200, strength=10)

selected_particle = None

running = True
paused = False

while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = env.find_particle(mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
            
    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        selected_particle.mouse_move((mouseX, mouseY))
    
    if not paused:
        env.update()
        
    screen.fill(env.colour)
    
    for p in env.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)
        
    for s in env.springs:
        pygame.draw.aaline(screen, (0, 0, 0), (int(s.p1.x), int(s.p1.y)), (int(s.p2.x), int(s.p2.y)))
        
    pygame.display.flip()