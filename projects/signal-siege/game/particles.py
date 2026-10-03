import random
import pygame


class Particle:
    def __init__(self, position, color, speed=180, life=0.45, size=4):
        self.position = pygame.Vector2(position)
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(1, 0).rotate(angle) * random.uniform(speed * 0.35, speed)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt):
        self.life -= dt
        self.position += self.velocity * dt
        self.velocity *= 0.92

    def draw(self, surface, offset):
        if self.life <= 0:
            return

        ratio = self.life / self.max_life
        radius = max(1, int(self.size * ratio))
        pygame.draw.circle(
            surface,
            self.color,
            self.position + offset,
            radius,
        )


def burst(particles, position, color, count=10, speed=180, size=4):
    for _ in range(count):
        particles.append(Particle(position, color, speed=speed, size=size))
