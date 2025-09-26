from constants import *
import pygame
import math
from circleshape import CircleShape
from items.inventory import Inventory
#from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, interface, item_spawner):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Initial rotation angle in degrees
        self.blink_timer = 0.0  # Timer for blink cooldown
        self.stamina = PLAYER_MAX_STAMINA  # Player stamina for sprinting
        self.stamina_recovery_cooldown = 0.0
        self.health = PLAYER_MAX_HEALTH  # Player health
        #self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.image = pygame.image.load("./images/player.png").convert_alpha()  # Use your image file here
        self.image = pygame.transform.smoothscale(self.image, (self.radius*2, self.radius*2))  # Optional: scale to fit
        self.image_rotation_offset = 0  # 0 if sprite faces up. try -90 if it faces right, +90 if it faces left.
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.inventory = Inventory(interface)
        self.item_spawner = item_spawner
        self.interface = interface
        self.interface.health = self.health
        self.interface.stamina = self.stamina
        self.immunity_timer = 0.0  # Timer for damage immunity

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.rotation + self.image_rotation_offset)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def rotate(self, dt, camera_offset=pygame.Vector2(0, 0)):
        mouse_pos = pygame.mouse.get_pos()
        # Convert player world position to screen position if you use a camera offset
        screen_pos = self.position - camera_offset
        direction = pygame.Vector2(mouse_pos) - screen_pos
        if direction.length_squared() == 0:
            return

        # Use the base forward vector that matches your sprite.
        # If your image faces up, use (0, -1). If it faces down, use (0, 1).
        base_forward = pygame.Vector2(0, -1)

        target_rotation = base_forward.angle_to(direction)

        # Calculate shortest angle difference and clamp rotation speed
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
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        new_position = self.position + forward * PLAYER_SPEED * dt
        playarea_center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
        if (new_position - playarea_center).length() + self.radius < PLAYAREA_RADIUS:
            self.position = new_position

    def strafe(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = forward.rotate(90)
        new_position = self.position + right * PLAYER_SPEED * dt / 2
        playarea_center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
        if (new_position - playarea_center).length() + self.radius < PLAYAREA_RADIUS:
            self.position = new_position

    def blinkForward(self):
        if self.blink_timer <= 0:
            forward = pygame.Vector2(0, -1).rotate(self.rotation)
            new_position = self.position + forward * PLAYER_SPEED * 1.1
            playarea_center = pygame.Vector2(PLAYAREA_RADIUS, PLAYAREA_RADIUS)
            if (new_position - playarea_center).length() + self.radius < PLAYAREA_RADIUS:
                self.position = new_position
            else:
                # Calculate maximum blink distance to stay within play area
                dir_to_edge = (new_position - playarea_center)
                if dir_to_edge.length() != 0:
                    direction = dir_to_edge.normalize()
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
        #self.interface.debugText = f"Alpha: {alpha:.2f}"
        self.image.set_alpha(alpha)

