import pygame
from constants import *
from items.item import Item

class Inventory:
    def __init__(self, interface):
        self.items = []
        self.interface = interface

    def add_item(self, item):
        if len(self.items) < INVENTORY_SIZE:  # Arbitrary inventory limit
            self.items.append(item)
            self.updateInventory()
            return True
        return False

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            item = self.items[index]
            self.items.pop(index)
            self.updateInventory()
            return item
        return None

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.items)

    def draw(self, screen):
        # Simple text-based inventory display
        font = pygame.font.Font(None, 36)
        y_offset = 10
        for item in self.items:
            text = font.render(f"{item.name} (Lvl {item.level})", True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += 40

    def updateInventory(self):
        self.interface.inventory = self.items

    def isFull(self):
        return len(self.items) >= INVENTORY_SIZE