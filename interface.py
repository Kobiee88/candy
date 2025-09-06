import pygame
from player import Player
from constants import PLAYER_MAX_STAMINA, PLAYER_MAX_HEALTH
from damage_sources.beam import Beam

class Interface:
    def __init__(self, player: Player, beam: Beam = None):
        self.player = player
        self.beam = beam
        self.font = pygame.font.SysFont(None, 34)

    def draw(self, screen):
        self.staminaBar(screen)
        self.healthBar(screen)
        if self.beam:
            self.displayBeamEndpointValues(screen)
        # For debugging: display beam endpoint values if a beam exists
        

    def add_internal(self, *args, **kwargs):
        pass  # or implement as needed

    def staminaBar(self, screen):
        # Draw stamina bar
        stamina_ratio = self.player.stamina / PLAYER_MAX_STAMINA
        stamina_bar_width = 220
        stamina_bar_height = 30
        stamina_bar_x = 15
        stamina_bar_y = 55

        pygame.draw.rect(screen, (232, 111, 107), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height))
        pygame.draw.rect(screen, (235, 212, 9), (stamina_bar_x, stamina_bar_y, stamina_bar_width * stamina_ratio, stamina_bar_height))

        # Draw stamina text
        stamina_text = self.font.render(f'Stamina: {self.player.stamina / PLAYER_MAX_STAMINA * 100:.0f} %', True, (0, 0, 0))
        screen.blit(stamina_text, (stamina_bar_x + 5, stamina_bar_y + 2))

    def healthBar(self, screen):
        # Draw health bar
        health_ratio = self.player.health / PLAYER_MAX_HEALTH
        health_bar_width = 220
        health_bar_height = 30
        health_bar_x = 15
        health_bar_y = 15

        pygame.draw.rect(screen, (232, 111, 107), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))

        # Draw health text
        health_text = self.font.render(f'Health: {self.player.health} / {PLAYER_MAX_HEALTH}', True, (0, 0, 0))
        screen.blit(health_text, (health_bar_x + 5, health_bar_y + 2))

    def displayBeamEndpointValues(self, screen):
        # Display beam endpoint coordinates for debugging
        endpoint = self.beam.returnEndpoint()
        endpoint_text = self.font.render(f'Beam Endpoint: ({int(endpoint.x)}, {int(endpoint.y)})', True, (255, 255, 255))
        screen.blit(endpoint_text, (15, 95))