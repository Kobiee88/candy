import pygame
from constants import *
import random

class Forge(pygame.sprite.Sprite):
    def __init__(self, position=(PLAYAREA_RADIUS, PLAYAREA_RADIUS)):
        super().__init__()
        self.image = pygame.image.load("./images/forge.png").convert_alpha()  # Use your image file here
        self.image = pygame.transform.smoothscale(self.image, (100, 100))  # Optional: scale to fit
        self.rect = self.image.get_rect(center=position)
        self.requestable_items = [
            {"name": "fire", "level": 1, "probability": 0.5},
            {"name": "water", "level": 1, "probability": 0.5},
        ]
        self.requestedItem = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        if not self.requestedItem:
            self.requestItem()

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
                self.requestedItem = item
                return item
        return None