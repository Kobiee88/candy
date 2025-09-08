import pygame
from constants import *

class Item(pygame.sprite.Sprite):
    def __init__(self, position, item_spawner, name="", level=1):
        super().__init__()
        self.image = pygame.image.load(f"./images/{name}_{level}.png").convert_alpha()  # Use your image file here
        self.image = pygame.transform.smoothscale(self.image, (ITEM_RADIUS*2, ITEM_RADIUS*2))  # Optional: scale to fit
        self.rect = self.image.get_rect(center=position)
        self.name = name
        self.level = level
        self.item_spawner = item_spawner
        self.lifetime = ITEM_LIFETIME
        self.pickup_cooldown = ITEM_PICKUP_COOLDOWN

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            self.item_spawner.activeItems -= 1
        if self.pickup_cooldown > 0:
            self.pickup_cooldown -= dt

    def canBePickedUp(self):
        return self.pickup_cooldown <= 0