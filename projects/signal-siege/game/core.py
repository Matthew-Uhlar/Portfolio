import random
import pygame

from . import settings
from .entities import Player, Bullet, Core, Enemy
from .particles import burst
from .storage import load_high_score, save_high_score
from .upgrades import choose_upgrades


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Signal Siege")

        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont("consolas", 18)
        self.font_medium = pygame.font.SysFont("consolas", 28, bold=True)
        self.font_large = pygame.font.SysFont("consolas", 54, bold=True)

        self.running = True
        self.high_score = load_high_score()
        self.reset()

    def reset(self):
        self.player = Player()
        self.core = Core()
        self.bullets = []
        self.enemies = []
        self.particles = []

        self.score = 0
        self.wave = 0
        self.wave_enemies_left = 0
        self.spawn_timer = 0.0
        self.spawn_delay = 0.65
        self.game_time = 0.0
        self.state = "playing"
        self.paused = False
        self.upgrade_choices = []
        self.message = ""
        self.message_timer = 0.0
        self.shake_strength = 0.0

        self.start_next_wave()

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000
            dt = min(dt, 0.033)

            self.handle_events()

            if not self.paused and self.state == "playing":
                self.update(dt)

            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state == "playing":
                    self.paused = not self.paused

                if event.key == pygame.K_r and self.state == "game_over":
                    self.reset()

                if self.state == "upgrade":
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        index = event.key - pygame.K_1
                        self.select_upgrade(index)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.state == "playing" and not self.paused:
                    self.try_shoot()

    def update(self, dt):
        self.game_time += dt
        self.message_timer = max(0, self.message_timer - dt)
        self.shake_strength = max(0, self.shake_strength - 18 * dt)

        self.player.update(dt)

        if pygame.mouse.get_pressed()[0]:
            self.try_shoot()

        self.update_wave(dt)

        for bullet in self.bullets:
            bullet.update(dt)

        for enemy in self.enemies:
            enemy.update(dt, self.core.position)

        self.handle_collisions(dt)

        for particle in self.particles:
            particle.update(dt)

        self.bullets = [bullet for bullet in self.bullets if bullet.alive]
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        self.particles = [particle for particle in self.particles if particle.life > 0]

        if self.player.health <= 0 or self.core.health <= 0:
            self.finish_game()

        if (
            self.wave_enemies_left == 0
            and not self.enemies
            and self.state == "playing"
        ):
            self.open_upgrade_screen()

    def try_shoot(self):
        # Only fire if the weapon cooldown is finished.
        if self.player.can_shoot(self.game_time):
            shots = self.player.shoot(pygame.mouse.get_pos(), self.game_time)
            self.bullets.extend(shots)
            burst(
                self.particles,
                self.player.position,
                settings.PLAYER_COLOR,
                count=3,
                speed=70,
                size=2,
            )

    def update_wave(self, dt):
        if self.wave_enemies_left <= 0:
            return

        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.wave_enemies_left -= 1
            self.spawn_timer = max(0.18, self.spawn_delay - self.wave * 0.018)

    def spawn_enemy(self):
        roll = random.random()

        if self.wave >= 5 and roll < 0.18:
            enemy_type = "tank"
        elif self.wave >= 2 and roll < 0.45:
            enemy_type = "fast"
        else:
            enemy_type = "normal"

        self.enemies.append(Enemy(self.wave, enemy_type))

    def handle_collisions(self, dt):
        for bullet in self.bullets:
            if not bullet.alive:
                continue

            for enemy in self.enemies:
                if not enemy.alive:
                    continue

                if bullet.position.distance_to(enemy.position) <= bullet.radius + enemy.radius:
                    enemy.take_damage(bullet.damage, self.particles)
                    bullet.remaining_hits -= 1

                    if bullet.remaining_hits <= 0:
                        bullet.alive = False

                    if not enemy.alive:
                        self.score += enemy.score_value

                    break

        for enemy in self.enemies:
            if not enemy.alive:
                continue

            if enemy.position.distance_to(self.player.position) <= enemy.radius + self.player.radius:
                if enemy.attack_timer <= 0:
                    self.player.take_damage(enemy.damage)
                    enemy.attack_timer = 0.65
                    self.shake_strength = 8
                    burst(
                        self.particles,
                        self.player.position,
                        settings.PLAYER_COLOR,
                        count=10,
                        speed=180,
                        size=4,
                    )

            if enemy.position.distance_to(self.core.position) <= enemy.radius + self.core.radius:
                if enemy.attack_timer <= 0:
                    self.core.take_damage(enemy.damage)
                    enemy.attack_timer = 0.8
                    self.shake_strength = 11
                    burst(
                        self.particles,
                        self.core.position,
                        settings.CORE_COLOR,
                        count=12,
                        speed=190,
                        size=4,
                    )

    def start_next_wave(self):
        self.wave += 1
        self.wave_enemies_left = 5 + self.wave * 3
        self.spawn_timer = 1.0
        self.message = f"WAVE {self.wave}"
        self.message_timer = 1.8
        self.player.shield = self.player.max_shield

    def open_upgrade_screen(self):
        self.state = "upgrade"
        self.upgrade_choices = choose_upgrades(3)

    def select_upgrade(self, index):
        if index < 0 or index >= len(self.upgrade_choices):
            return

        upgrade = self.upgrade_choices[index]
        upgrade["apply"](self.player, self.core)
        self.state = "playing"
        self.start_next_wave()

    def finish_game(self):
        self.state = "game_over"

        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    def draw(self):
        offset = pygame.Vector2(0, 0)

        if self.shake_strength > 0:
            offset.x = random.uniform(-self.shake_strength, self.shake_strength)
            offset.y = random.uniform(-self.shake_strength, self.shake_strength)

        self.screen.fill(settings.BACKGROUND)
        self.draw_grid(offset)

        self.core.draw(self.screen, self.game_time, offset)

        for bullet in self.bullets:
            bullet.draw(self.screen, offset)

        for enemy in self.enemies:
            enemy.draw(self.screen, offset)

        self.player.draw(self.screen, pygame.mouse.get_pos(), offset)

        for particle in self.particles:
            particle.draw(self.screen, offset)

        self.draw_hud()

        if self.message_timer > 0:
            self.draw_center_message(self.message)

        if self.paused:
            self.draw_overlay("PAUSED", "Press Escape to continue")

        if self.state == "upgrade":
            self.draw_upgrade_screen()

        if self.state == "game_over":
            reason = "The communication core was lost." if self.core.health <= 0 else "Your suit failed."
            self.draw_overlay(
                "SIGNAL LOST",
                f"{reason}  Score: {self.score}  Press R to restart",
            )

        pygame.display.flip()

    def draw_grid(self, offset):
        spacing = 50

        for x in range(-spacing, settings.WIDTH + spacing, spacing):
            pygame.draw.line(
                self.screen,
                settings.GRID,
                (x + offset.x, 0),
                (x + offset.x, settings.HEIGHT),
            )

        for y in range(-spacing, settings.HEIGHT + spacing, spacing):
            pygame.draw.line(
                self.screen,
                settings.GRID,
                (0, y + offset.y),
                (settings.WIDTH, y + offset.y),
            )

    def draw_hud(self):
        self.draw_bar(24, 24, 260, 18, self.player.health, self.player.max_health, settings.HEALTH_COLOR)
        self.draw_bar(24, 50, 260, 11, self.player.shield, self.player.max_shield, settings.SHIELD_COLOR)
        self.draw_bar(
            settings.WIDTH - 284,
            24,
            260,
            18,
            self.core.health,
            self.core.max_health,
            settings.CORE_COLOR,
        )

        player_text = self.font_small.render("PLAYER", True, settings.WHITE)
        core_text = self.font_small.render("CORE", True, settings.WHITE)
        score_text = self.font_medium.render(f"SCORE {self.score}", True, settings.WHITE)
        wave_text = self.font_small.render(
            f"WAVE {self.wave}   ENEMIES {self.wave_enemies_left + len(self.enemies)}",
            True,
            settings.MUTED,
        )
        high_score_text = self.font_small.render(
            f"HIGH SCORE {self.high_score}",
            True,
            settings.MUTED,
        )

        self.screen.blit(player_text, (24, 70))
        self.screen.blit(core_text, (settings.WIDTH - 284, 50))
        self.screen.blit(score_text, score_text.get_rect(center=(settings.WIDTH / 2, 32)))
        self.screen.blit(wave_text, wave_text.get_rect(center=(settings.WIDTH / 2, 62)))
        self.screen.blit(high_score_text, (24, settings.HEIGHT - 34))

    def draw_bar(self, x, y, width, height, value, maximum, color):
        ratio = 0 if maximum <= 0 else max(0, min(1, value / maximum))
        pygame.draw.rect(
            self.screen,
            settings.PANEL,
            (x, y, width, height),
            border_radius=height // 2,
        )
        pygame.draw.rect(
            self.screen,
            color,
            (x, y, width * ratio, height),
            border_radius=height // 2,
        )

    def draw_center_message(self, text):
        label = self.font_large.render(text, True, settings.WHITE)
        self.screen.blit(label, label.get_rect(center=(settings.WIDTH / 2, 130)))

    def draw_overlay(self, title, subtitle):
        # Darken the background so the menu stands out.
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 8, 15, 210))
        self.screen.blit(overlay, (0, 0))

        title_label = self.font_large.render(title, True, settings.WHITE)
        subtitle_label = self.font_small.render(subtitle, True, settings.MUTED)

        self.screen.blit(title_label, title_label.get_rect(center=(settings.WIDTH / 2, settings.HEIGHT / 2 - 30)))
        self.screen.blit(subtitle_label, subtitle_label.get_rect(center=(settings.WIDTH / 2, settings.HEIGHT / 2 + 28)))

    def draw_upgrade_screen(self):
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 8, 15, 225))
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("CHOOSE AN UPGRADE", True, settings.WHITE)
        subtitle = self.font_small.render(
            "Press 1, 2 or 3 to continue",
            True,
            settings.MUTED,
        )

        self.screen.blit(title, title.get_rect(center=(settings.WIDTH / 2, 120)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(settings.WIDTH / 2, 165)))

        card_width = 290
        card_height = 250
        gap = 28
        start_x = (settings.WIDTH - (card_width * 3 + gap * 2)) / 2

        for index, upgrade in enumerate(self.upgrade_choices):
            x = start_x + index * (card_width + gap)
            y = 225
            rect = pygame.Rect(x, y, card_width, card_height)

            pygame.draw.rect(self.screen, settings.PANEL, rect, border_radius=16)
            pygame.draw.rect(self.screen, settings.PANEL_BORDER, rect, 2, border_radius=16)

            number = self.font_medium.render(str(index + 1), True, settings.CORE_COLOR)
            name = self.font_medium.render(upgrade["name"], True, settings.WHITE)
            description = self.wrap_text(upgrade["description"], card_width - 40)

            self.screen.blit(number, (x + 20, y + 18))
            self.screen.blit(name, (x + 20, y + 70))

            for line_index, line in enumerate(description):
                label = self.font_small.render(line, True, settings.MUTED)
                self.screen.blit(label, (x + 20, y + 125 + line_index * 26))

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = f"{current} {word}".strip()

            if self.font_small.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines
