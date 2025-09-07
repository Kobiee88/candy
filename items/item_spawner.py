import pygame
from constants import *
from items.item import Item
import random

class ItemSpawner:
    def __init__(self, draw_container, update_container, item_container):
        #self.spawn_area_radius = spawn_area_radius
        #self.items = pygame.sprite.Group()
        super().__init__()
        self.activeItems = 0
        self.draw_container = draw_container
        self.update_container = update_container
        self.item_container = item_container
        self.spawn_cooldown = 0

    def spawn_item(self, name, level):
        angle = random.uniform(0, 360)
        distance = random.uniform(0, PLAYAREA_RADIUS - ITEM_RADIUS)
        spawn_x = PLAYAREA_RADIUS + distance * pygame.math.Vector2(1, 0).rotate(angle).x
        spawn_y = PLAYAREA_RADIUS + distance * pygame.math.Vector2(1, 0).rotate(angle).y
        item = Item((spawn_x, spawn_y), self, name, level)
        self.activeItems += 1
        self.spawn_cooldown = ITEM_SPAWN_COOLDOWN
        #self.items.add(item)
        return item

    def update(self, dt):
        #self.items.update(dt)
        self.spawn_cooldown -= dt
        if self.spawn_cooldown > 0:
            return
        if self.activeItems >= ITEM_LIMIT:
            return
        if random.random() > ITEM_SPAWN_CHANCE:
            return
        item = self.spawn_item("fire", 1)
        self.draw_container.add(item)
        self.update_container.add(item)
        self.item_container.add(item)

    def add_internal(self, *args, **kwargs):
        pass  # or implement as needed