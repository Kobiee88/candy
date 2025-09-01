from constants import *
import pygame
from circleshape import CircleShape

class Playarea(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYAREA_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)  # Draw the play area boundary in white

    def update(self, dt):
        pass