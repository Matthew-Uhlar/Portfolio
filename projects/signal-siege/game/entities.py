import math
import random
import pygame

from . import settings
from .particles import burst


class Player:
    def __init__(self):
        self.position = pygame.Vector2(settings.WIDTH / 2, settings.HEIGHT / 2 + 160)
        self.radius = settings.PLAYER_RADIUS
        self.speed = settings.PLAYER_SPEED
        self.max_health = settings.PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.max_shield = settings.PLAYER_MAX_SHIELD
        self.shield = self.max_shield
        self.damage = settings.BULLET_DAMAGE
        self.shot_delay = settings.SHOT_DELAY
        self.last_shot = 0.0
        self.multishot = 1
        self.piercing = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w],
        )

        if movement.length_squared() > 0:
            movement = movement.normalize()

        self.position += movement * self.speed * dt
        self.position.x = max(self.radius, min(settings.WIDTH - self.radius, self.position.x))
        self.position.y = max(self.radius, min(settings.HEIGHT - self.radius, self.position.y))

    def can_shoot(self, game_time):
        return game_time - self.last_shot >= self.shot_delay

    def shoot(self, target, game_time):
        self.last_shot = game_time
        base_direction = pygame.Vector2(target) - self.position

        if base_direction.length_squared() == 0:
            base_direction = pygame.Vector2(1, 0)

        base_direction = base_direction.normalize()
        spread = 9
        bullets = []

        for index in range(self.multishot):
            center = (self.multishot - 1) / 2
            angle = (index - center) * spread
            direction = base_direction.rotate(angle)
            bullets.append(
                Bullet(
                    self.position + direction * (self.radius + 8),
                    direction,
                    self.damage,
                    self.piercing,
                )
            )

        return bullets

    def take_damage(self, amount):
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed

        self.health = max(0, self.health - amount)

    def draw(self, surface, mouse_position, offset):
        position = self.position + offset
        direction = pygame.Vector2(mouse_position) - self.position

        # Keep things from breaking if the mouse is directly on the player.
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)

        direction = direction.normalize()
        side = direction.rotate(90)

        points = [
            position + direction * 25,
            position - direction * 16 + side * 14,
            position - direction * 9,
            position - direction * 16 - side * 14,
        ]

        pygame.draw.polygon(surface, settings.PLAYER_COLOR, points)
        pygame.draw.circle(surface, settings.WHITE, position, 6)


class Bullet:
    def __init__(self, position, direction, damage, piercing):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(direction) * settings.BULLET_SPEED
        self.radius = settings.BULLET_RADIUS
        self.damage = damage
        self.remaining_hits = 1 + piercing
        self.alive = True

    def update(self, dt):
        self.position += self.velocity * dt

        margin = 30
        if (
            self.position.x < -margin
            or self.position.x > settings.WIDTH + margin
            or self.position.y < -margin
            or self.position.y > settings.HEIGHT + margin
        ):
            self.alive = False

    def draw(self, surface, offset):
        pygame.draw.circle(
            surface,
            settings.BULLET_COLOR,
            self.position + offset,
            self.radius,
        )


class Core:
    def __init__(self):
        self.position = pygame.Vector2(settings.WIDTH / 2, settings.HEIGHT / 2)
        self.radius = settings.CORE_RADIUS
        self.max_health = settings.CORE_MAX_HEALTH
        self.health = self.max_health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def draw(self, surface, game_time, offset):
        position = self.position + offset
        pulse = 4 + math.sin(game_time * 4) * 3

        pygame.draw.circle(
            surface,
            settings.CORE_COLOR,
            position,
            self.radius + int(pulse),
            3,
        )
        pygame.draw.circle(surface, settings.PANEL, position, self.radius)
        pygame.draw.circle(surface, settings.CORE_COLOR, position, 18)
        pygame.draw.circle(surface, settings.WHITE, position, 6)


class Enemy:
    def __init__(self, wave, enemy_type="normal"):
        self.enemy_type = enemy_type
        self.position = self._spawn_position()
        self.alive = True
        self.attack_timer = 0.0

        health_scale = 1 + (wave - 1) * 0.12
        speed_scale = 1 + min(0.5, (wave - 1) * 0.025)

        if enemy_type == "fast":
            self.radius = 13
            self.max_health = 38 * health_scale
            self.speed = 150 * speed_scale
            self.damage = 8
            self.color = settings.FAST_ENEMY_COLOR
            self.score_value = 20
        elif enemy_type == "tank":
            self.radius = 26
            self.max_health = 150 * health_scale
            self.speed = 58 * speed_scale
            self.damage = 20
            self.color = settings.TANK_ENEMY_COLOR
            self.score_value = 40
        else:
            self.radius = 18
            self.max_health = 70 * health_scale
            self.speed = 92 * speed_scale
            self.damage = 12
            self.color = settings.ENEMY_COLOR
            self.score_value = 10

        self.health = self.max_health

    def _spawn_position(self):
        margin = 45
        side = random.randrange(4)

        if side == 0:
            return pygame.Vector2(random.uniform(0, settings.WIDTH), -margin)
        if side == 1:
            return pygame.Vector2(settings.WIDTH + margin, random.uniform(0, settings.HEIGHT))
        if side == 2:
            return pygame.Vector2(random.uniform(0, settings.WIDTH), settings.HEIGHT + margin)

        return pygame.Vector2(-margin, random.uniform(0, settings.HEIGHT))

    def update(self, dt, target):
        direction = pygame.Vector2(target) - self.position

        if direction.length_squared() > 0:
            self.position += direction.normalize() * self.speed * dt

        self.attack_timer = max(0, self.attack_timer - dt)

    def take_damage(self, amount, particles):
        self.health -= amount
        burst(particles, self.position, self.color, count=4, speed=100, size=3)

        if self.health <= 0:
            self.alive = False
            burst(particles, self.position, self.color, count=16, speed=220, size=5)

    def draw(self, surface, offset):
        position = self.position + offset

        if self.enemy_type == "tank":
            rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
            rect.center = position
            pygame.draw.rect(surface, self.color, rect, border_radius=7)
        elif self.enemy_type == "fast":
            points = [
                position + pygame.Vector2(0, -self.radius),
                position + pygame.Vector2(self.radius, self.radius),
                position + pygame.Vector2(-self.radius, self.radius),
            ]
            pygame.draw.polygon(surface, self.color, points)
        else:
            pygame.draw.circle(surface, self.color, position, self.radius)

        health_ratio = max(0, self.health / self.max_health)
        bar_width = self.radius * 2
        bar = pygame.Rect(
            position.x - self.radius,
            position.y - self.radius - 10,
            bar_width,
            4,
        )
        pygame.draw.rect(surface, (45, 52, 67), bar)
        pygame.draw.rect(
            surface,
            settings.HEALTH_COLOR,
            (bar.x, bar.y, bar_width * health_ratio, bar.height),
        )
