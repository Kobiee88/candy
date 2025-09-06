import pygame
from constants import *

class Meteor(pygame.sprite.Sprite):
    def __init__(self, position, player):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.surface = pygame.Surface((METEOR_RADIUS * 2, METEOR_RADIUS * 2), pygame.SRCALPHA)
        self.surface.set_alpha(0)  # Fully transparent initially
        pygame.draw.circle(self.surface, (139, 69, 19), (METEOR_RADIUS, METEOR_RADIUS), METEOR_RADIUS)  # Brown circle as meteor
        self.rect = self.surface.get_rect(center=self.position)

        self.spawn_timer = METEOR_SPAWN_TIMER
        self.target = player

    def update(self, dt):
        if self.spawn_timer > 0:
            self.spawn_timer -= dt
            self.surface.set_alpha(self.surface.get_alpha() + dt * 255 / METEOR_SPAWN_TIMER)
        else:
            if self.check_collision(self.target):
                self.target.take_damage(METEOR_DAMAGE)
            self.kill()
            

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def check_collision(self, player):
        distance = self.position.distance_to(player.position)
        if distance < METEOR_RADIUS + PLAYER_RADIUS:
            return True
        return False