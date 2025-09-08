from constants import *
import pygame
import math
from circleshape import CircleShape
from items.inventory import Inventory
from interface import Interface
from items.item_spawner import ItemSpawner
#from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, interface, item_spawner):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Initial rotation angle in degrees
        self.blink_timer = 0.0  # Timer for blink cooldown
        self.stamina = PLAYER_MAX_STAMINA  # Player stamina for sprinting
        self.stamina_recovery_cooldown = 0.0
        self.health = PLAYER_MAX_HEALTH  # Player health
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.inventory = Inventory(interface)
        self.item_spawner = item_spawner
        self.interface = interface
        self.interface.health = self.health
        self.interface.stamina = self.stamina
        self.immunity_timer = 0.0  # Timer for damage immunity
        #self.image = pygame.image.load("./images/player.png").convert_alpha()  # Use your image file here
        #self.image = pygame.transform.smoothscale(self.image, (self.radius*2, self.radius*2))  # Optional: scale to fit

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)  # Draw the player triangle in white
        #rotated_image = pygame.transform.rotate(self.image, self.rotation)
        #rect = rotated_image.get_rect(center=self.position)
        #screen.blit(rotated_image, rect)

    def rotate(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos) - self.position
        target_rotation = -direction.angle_to(pygame.Vector2(0, 1))

        # Calculate shortest angle difference
        diff = (target_rotation - self.rotation + 180) % 360 - 180
        max_step = PLAYER_TURN_SPEED * dt
        if abs(diff) < max_step:
            self.rotation = target_rotation
        else:
            self.rotation += max_step if diff > 0 else -max_step
            self.rotation %= 360

    def update(self, dt):
        keys = pygame.key.get_pressed()
        speed = 1
        self.blink_timer -= dt
        if self.stamina_recovery_cooldown > 0:
            self.stamina_recovery_cooldown -= dt
        else:
            if self.stamina < PLAYER_MAX_STAMINA:
                self.stamina += PLAYER_STAMINA_RECOVERY_RATE * dt
                if self.stamina > PLAYER_MAX_STAMINA:
                    self.stamina = PLAYER_MAX_STAMINA
        
        if self.immunity_timer > 0:
            self.immunity_timer -= dt
            self.imageFlicker(dt)

        self.rotate(dt)

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed = self.sprint(dt)
        
        if keys[pygame.K_a]:
            self.strafe(-dt * speed)
        if keys[pygame.K_d]:
            self.strafe(dt * speed)
        if keys[pygame.K_w]:
            self.move(dt * speed)
        if keys[pygame.K_s]:
            self.move(-dt * speed)
        if keys[pygame.K_SPACE]:
            self.blinkForward()
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.interface.health = self.health
        self.interface.stamina = self.stamina

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        new_position = self.position + forward * PLAYER_SPEED * dt
        playarea_center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
        if (new_position - playarea_center).length() + self.radius < PLAYAREA_RADIUS:
            self.position = new_position

    def strafe(self, dt):
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        new_position = self.position + right * PLAYER_SPEED * dt / 2
        playarea_center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
        if (new_position - playarea_center).length() + self.radius < PLAYAREA_RADIUS:
            self.position = new_position

    def blinkForward(self):
        if self.blink_timer <= 0:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            new_position = self.position + forward * PLAYER_SPEED * 0.8
            playarea_center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
            if (new_position - playarea_center).length() + self.radius < PLAYAREA_RADIUS:
                self.position = new_position
            else:
                # Calculate maximum blink distance to stay within play area
                direction = (new_position - playarea_center).normalize()
                max_distance = PLAYAREA_RADIUS - self.radius - (self.position - playarea_center).length()
                self.position += direction * max_distance
            self.blink_timer = PLAYER_BLINK_COOLDOWN

    def sprint(self, dt):
        if self.stamina > 0:
            self.stamina -= dt
            self.stamina_recovery_cooldown = 1.0
            return PLAYER_SPRINT_FACTOR
        elif self.stamina_recovery_cooldown <= 0:
            self.stamina_recovery_cooldown = 1.0
        return 1.0
    
    def take_damage(self, amount):
        if self.immunity_timer > 0:
            return  # Still immune, ignore damage
        self.health -= amount
        self.immunity_timer = PLAYER_IMMUNITY_TIME
        if self.health < 0:
            self.health = 0
        # You can add additional logic here, such as triggering a death event if health reaches 0

    def dropItem(self, index):
        removed_item = self.inventory.remove_item(index)
        if removed_item:
            self.item_spawner.spawn_item(removed_item.name, removed_item.level, self.position + pygame.Vector2(0, -self.radius*2).rotate(self.rotation))

    # Not working as intended yet - Player has no own surface
    def imageFlicker(self, dt):
        alpha = self.image.get_alpha()
        alpha = 128 + 127 * math.sin((PLAYER_IMMUNITY_TIME - self.immunity_timer) * 20)
        self.interface.debugText = f"Alpha: {alpha:.2f}"
        self.image.set_alpha(alpha)

