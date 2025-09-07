import pygame
from constants import *

class Beam(pygame.sprite.Sprite):
    def __init__(self, rotation = 0, speed=50, length=PLAYAREA_RADIUS, width=10):
        super().__init__()
        self.center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
        self.angle = rotation  # Initial angle in degrees
        self.speed = speed
        self.length = length
        self.width = width
        self.active = False
        self.spawn_timer = EVENT_SPAWN_TIMER

        # Create a transparent surface for the beam
        self.surface = pygame.Surface((length * 2, width), pygame.SRCALPHA)
        self.surface.set_alpha(0)  # Fully transparent initially
        self.rotated_surface = self.surface
        # Draw the beam from left (0, width//2) to right (length, width//2)
        pygame.draw.line(
            self.surface,
            (255, 0, 0),
            (0, width // 2),
            (length, width // 2),
            width
        )
        #self.image = self.image_orig
        # The rect's topleft will be adjusted in update()
        self.rect = self.surface.get_rect(center=self.center)

    def update(self, dt):
        if not self.active:
            self.spawn_timer -= dt
            self.rotated_surface.set_alpha(self.surface.get_alpha() + dt * 240 / EVENT_SPAWN_TIMER)
            if self.spawn_timer <= 0:
                self.active = True
            else:
                return
        else:
            self.angle += self.speed * dt  # speed is degrees per second
            self.angle %= 360
            # Rotate the beam image
            self.rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
            self.rect = self.rotated_surface.get_rect(center=self.center)

    def draw(self, screen):
        screen.blit(self.rotated_surface, self.rect)

    def returnEndpoint(self):
        # Calculate the endpoint of the beam based on its angle and length
        direction = pygame.Vector2(-1, 0).rotate(self.angle)
        endpoint = self.center + direction * self.length
        return endpoint