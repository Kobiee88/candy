import pygame
from constants import *
import random

import interface
from items.item import Item

class Forge(pygame.sprite.Sprite):
    def __init__(self, interface, player):
        super().__init__()
        self.image = pygame.image.load("./images/forge.png").convert_alpha()  # Use your image file here
        self.image = pygame.transform.smoothscale(self.image, (100, 100))  # Optional: scale to fit
        self.rect = self.image.get_rect(center=(PLAYAREA_RADIUS, PLAYAREA_RADIUS))
        self.interface = interface
        self.player = player
        self.requestable_items = [
            {"name": "fire", "level": 1, "probability": 0.5},
            {"name": "water", "level": 1, "probability": 0.5},
            {"name": "nature", "level": 1, "probability": 0.5},
        ]
        self.requestedItem = None
        self.request_cooldown = 0.0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        if not self.requestedItem and self.request_cooldown <= 0.0:
            self.interface.updateRequestedItem(self.requestItem())
        self.turnInItem()
        if self.request_cooldown > 0.0:
            self.request_cooldown -= dt
            self.interface.updateRequestCooldown(self.request_cooldown)

    def changeProbability(self, item_name, item_level, new_probability):
        for item in self.requestable_items:
            if item["name"] == item_name and item["level"] == item_level:
                item["probability"] = new_probability
                return
        self.requestable_items.append({"name": item_name, "level": item_level, "probability": new_probability})

    def requestItem(self):
        if len(self.requestable_items) == 0:
            return None
        total_probability = sum(item["probability"] for item in self.requestable_items)
        rand_value = random.uniform(0, total_probability)
        cumulative_probability = 0
        for item in self.requestable_items:
            cumulative_probability += item["probability"]
            if rand_value <= cumulative_probability:
                self.requestedItem = Item((0, 0), self, item["name"], item["level"])
                return self.requestedItem
        return None
    
    def turnInItem(self):
        if not self.requestedItem:
            return False
        if not self.checkPlayerInRange():
            return False
        for i, item in enumerate(self.player.inventory.items):
            if item.name == self.requestedItem.name and item.level == self.requestedItem.level:
                self.player.inventory.remove_item(i)
                self.requestedItem = None
                self.interface.updateRequestedItem(None)
                self.interface.updatePoints(10 * item.level * item.level)  # Award points based on item level
                self.request_cooldown = FORGE_REQUEST_COOLDOWN
                self.interface.updateRequestCooldown(self.request_cooldown)
                return True
        return False
    
    def checkPlayerInRange(self):
        distance = self.player.position.distance_to(pygame.Vector2(self.rect.center))
        return distance <= FORGE_RADIUS + self.player.radius