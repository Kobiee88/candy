import pygame
from constants import *
from damage_sources.beam import Beam

class Interface:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 34)
        self.health = 0
        self.stamina = 0
        self.inventory = []  # Placeholder for inventory items
        self.debugText = ""
        self.timer = 0
        self.points = 0
        self.requestedItem = None
        self.requestCooldown = 0.0

    def draw(self, screen):
        self.staminaBar(screen)
        self.healthBar(screen)
        self.draw_inventory(screen)
        self.debugConsole(screen)  # Add any debug text you want to display
        self.displayTimer(screen)
        self.displayPoints(screen)
        self.drawRequestedItem(screen)

    def add_internal(self, *args, **kwargs):
        pass  # or implement as needed

    def staminaBar(self, screen):
        # Draw stamina bar
        stamina_ratio = self.stamina / PLAYER_MAX_STAMINA
        stamina_bar_width = 220
        stamina_bar_height = 30
        stamina_bar_x = 15
        stamina_bar_y = 55

        pygame.draw.rect(screen, (232, 111, 107), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height))
        pygame.draw.rect(screen, (235, 212, 9), (stamina_bar_x, stamina_bar_y, stamina_bar_width * stamina_ratio, stamina_bar_height))

        # Draw stamina text
        stamina_text = self.font.render(f'Stamina: {abs(self.stamina / PLAYER_MAX_STAMINA * 100):.0f} %', True, (0, 0, 0))
        screen.blit(stamina_text, (stamina_bar_x + 5, stamina_bar_y + 2))

    def healthBar(self, screen):
        # Draw health bar
        health_ratio = self.health / PLAYER_MAX_HEALTH
        health_bar_width = 220
        health_bar_height = 30
        health_bar_x = 15
        health_bar_y = 15

        pygame.draw.rect(screen, (232, 111, 107), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))

        # Draw health text
        health_text = self.font.render(f'Health: {self.health} / {PLAYER_MAX_HEALTH}', True, (0, 0, 0))
        screen.blit(health_text, (health_bar_x + 5, health_bar_y + 2))

    def debugConsole(self, screen, text=None):
        debug_text = self.font.render(f'DEBUG: ({self.debugText})', True, (255, 255, 255))
        screen.blit(debug_text, (15, 95))

    def draw_inventory(self, screen):
        x_offset = 0
        for i in range(INVENTORY_SIZE):
            text_color = (200, 200, 200)
            if i < len(self.inventory):
                item_image = pygame.transform.smoothscale(self.inventory[i].image, (50, 50))
                screen.blit(item_image, (SCREEN_WIDTH - 60 * INVENTORY_SIZE + x_offset, SCREEN_HEIGHT - 60))
                text_color = (10, 10, 10)  # Change text color for better visibility
            else:
                # Draw slot rectangle
                slot_rect = pygame.Rect(SCREEN_WIDTH - 60 * INVENTORY_SIZE + x_offset, SCREEN_HEIGHT - 60, 50, 50)
                pygame.draw.rect(screen, (50, 50, 50), slot_rect)
            # Draw slot number
            num_text = self.font.render(str(i + 1), True, text_color)
            # Position number in the top-left of the slot with a small margin
            screen.blit(num_text, (SCREEN_WIDTH - 60 * INVENTORY_SIZE + x_offset + 4, SCREEN_HEIGHT - 60 + 2))
            x_offset += 60

    def drawRequestedItem(self, screen):
        request_text = self.font.render(f'CENTER:', True, (255, 255, 255))
        screen.blit(request_text, (30, SCREEN_HEIGHT - 170))
        if self.requestedItem:
            item_image = pygame.transform.smoothscale(self.requestedItem.image, (100, 100))
            screen.blit(item_image, (30, SCREEN_HEIGHT - 140))
            item_text = self.font.render(f'Requested: {self.requestedItem.name.capitalize()} ({self.requestedItem.level})', True, (255, 255, 255))
            screen.blit(item_text, (30, SCREEN_HEIGHT - 30))
        else:
            slot_rect = pygame.Rect(30, SCREEN_HEIGHT - 140, 100, 100)
            pygame.draw.rect(screen, (50, 50, 50), slot_rect)
            cooldown_text = self.font.render(f'{self.requestCooldown:.1f}s', True, (255, 255, 255))
            screen.blit(cooldown_text, (55, SCREEN_HEIGHT - 115))

    def update(self, dt):
        self.timer += dt
    
    def displayTimer(self, screen):
        timer_text = self.font.render(f'Time: {self.timer:.2f} s', True, (255, 255, 255))
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 15))

    def displayPoints(self, screen):
        points_text = self.font.render(f'Points: {self.points}', True, (255, 255, 255))
        screen.blit(points_text, (SCREEN_WIDTH - 150, 55))

    def updateRequestedItem(self, item):
        self.requestedItem = item

    def updateRequestCooldown(self, cooldown):
        self.requestCooldown = cooldown

    def updatePoints(self, points):
        self.points += points
