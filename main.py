import pygame
import sys
import random
from constants import *
from player import Player
from playarea import Playarea
from interface import Interface
from damage_sources.beam import Beam
from damage_sources.meteor import Meteor

def main():
    pygame.init()
    pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    #asteroids = pygame.sprite.Group()
    #shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    #Asteroid.containers = (asteroids, updatable, drawable)
    #AsteroidField.containers = (updatable)
    #Shot.containers = (shots, updatable, drawable)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    playarea = Playarea(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    drawable.add(playarea)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)  # Create player at center of screen
    beam = Beam()  # Example beam
    updatable.add(beam)
    drawable.add(beam)
    interface = Interface(player, beam)
    drawable.add(interface)
    #asteroid_field = AsteroidField()  # Create asteroid field
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen, (0, 0, 0))  # Fill the screen with black
        for item in drawable:
            item.draw(screen)
        updatable.update(dt)
        '''for asteroid in asteroids:
            if asteroid.check_collision(player):
                print("Game over!")
                sys.exit()
            else:
                for shot in shots:
                    if asteroid.check_collision(shot):
                        shot.kill()
                        asteroid.split()'''
        if random.random() < METEOR_SPAWN_CHANCE and len(updatable.sprites()) < 10:
            angle = random.uniform(0, 360)
            distance = random.uniform(0, PLAYAREA_RADIUS)
            spawn_x = PLAYAREA_RADIUS + distance * pygame.math.Vector2(1, 0).rotate(angle).x
            spawn_y = PLAYAREA_RADIUS + distance * pygame.math.Vector2(1, 0).rotate(angle).y
            meteor = Meteor((spawn_x, spawn_y), player)
            updatable.add(meteor)
            drawable.add(meteor)
        beam_clipped = player.rect.clipline(PLAYAREA_RADIUS, PLAYAREA_RADIUS, beam.returnEndpoint().x, beam.returnEndpoint().y)
        if beam.active and beam_clipped:
            player.take_damage(1)
        pygame.display.flip()  # Update the display
        dt = pygame.time.Clock().tick(60) / 1000  # Limit to 60 FPS


if __name__ == "__main__":
    main()