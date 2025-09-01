import pygame
from player import Player
from constants import PLAYER_MAX_STAMINA

class Interface:
    def __init__(self, player: Player):
        self.player = player
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        self.staminaBar(screen)

    def add_internal(self, *args, **kwargs):
        pass  # or implement as needed

    def staminaBar(self, screen):
        # Draw stamina bar
        stamina_ratio = self.player.stamina / PLAYER_MAX_STAMINA
        stamina_bar_width = 220
        stamina_bar_height = 30
        stamina_bar_x = 15
        stamina_bar_y = 15

        pygame.draw.rect(screen, (255, 0, 0), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (stamina_bar_x, stamina_bar_y, stamina_bar_width * stamina_ratio, stamina_bar_height))

        # Draw stamina text
        stamina_text = self.font.render(f'Stamina: {self.player.stamina:.1f}/5.0', True, (0, 0, 0))
        screen.blit(stamina_text, (stamina_bar_x + 5, stamina_bar_y + 2))