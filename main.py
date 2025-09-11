import pygame
import sys
import random
from constants import *
from player import Player
from playarea import Playarea
from interface import Interface
from damage_sources.beam import Beam
from damage_sources.meteor import Meteor
#from items.item import Item
from items.item_spawner import ItemSpawner
from items.forge import Forge

def main():
    pygame.init()
    pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    items = pygame.sprite.Group()
    beam = Beam()  # Example beam
    updatable.add(beam)
    drawable.add(beam)
    interface = Interface(beam)
    drawable.add(interface)
    updatable.add(interface)
    Player.containers = (updatable, drawable)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    playarea = Playarea(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    drawable.add(playarea)
    item_spawner = ItemSpawner(drawable, updatable, items)
    updatable.add(item_spawner)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, interface, item_spawner)  # Create player at center of screen
    forge = Forge()
    drawable.add(forge)
    updatable.add(forge)
    #item = Item((SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT / 2), "fire", 1)
    #drawable.add(item)
    #asteroid_field = AsteroidField()  # Create asteroid field
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_1:
                    player.dropItem(0)
                if event.key == pygame.K_2:
                    player.dropItem(1)
                if event.key == pygame.K_3:
                    player.dropItem(2)
        pygame.Surface.fill(screen, (0, 0, 0))  # Fill the screen with black
        for item in drawable:
            item.draw(screen)
        updatable.update(dt)
        for item in items:
            if not item.canBePickedUp():
                continue
            if item.rect.colliderect(player.rect):
                if not player.inventory.isFull():
                    player.inventory.add_item(item)
                    item.kill()
                    item_spawner.activeItems -= 1
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
            distance = random.uniform(FORGE_RADIUS + METEOR_RADIUS, PLAYAREA_RADIUS)
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