# A game developed with Python based on physics concepts.
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
import math


class Spring:
    def __init__(self, p1, p2, length=100, strength=0.9):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.strength = strength

    def update(self):
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        force = (self.length - dist) * self.strength

        self.p1.accelerate((theta + 0.5 * math.pi, force / self.p1.mass))
        self.p2.accelerate((theta - 0.5 * math.pi, force / self.p2.mass))