import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ships.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Movement
        self.moving_right = self.moving_left = False
        self.moving_up = self.moving_down = False

        # Skill last-used timestamps
        self.last_q = self.last_w = self.last_e = self.last_r = 0

        # Skill states
        self.has_shield = False
        self.is_cloned = False
        self.clone_start_time = 0
        self.show_explosion = False
        self.explosion_start_time = 0

        # Power-up states
        self.double_damage = False
        self.double_damage_end = 0
        self.rapid_fire = False
        self.rapid_fire_end = 0

    def center_ship(self) -> None:
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10
        self.centery = float(self.rect.centery)

    def apply_powerup(self, kind: str) -> None:
        now = pygame.time.get_ticks()
        if kind == 'double_damage':
            self.double_damage = True
            self.double_damage_end = now + self.ai_settings.double_damage_duration
        elif kind == 'rapid_fire':
            self.rapid_fire = True
            self.rapid_fire_end = now + self.ai_settings.rapid_fire_duration

    def update(self) -> None:
        spd = self.ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += spd
        if self.moving_left and self.rect.left > 0:
            self.center -= spd
        if self.moving_up and self.rect.top > 0:
            self.centery -= spd
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += spd

        self.rect.centerx = self.center
        self.rect.centery = self.centery

        now = pygame.time.get_ticks()
        if self.is_cloned and now - self.clone_start_time > self.ai_settings.clone_duration:
            self.is_cloned = False
        if self.double_damage and now > self.double_damage_end:
            self.double_damage = False
        if self.rapid_fire and now > self.rapid_fire_end:
            self.rapid_fire = False

    def blitme(self) -> None:
        # Clone ghosts (semi-transparent)
        if self.is_cloned:
            ghost = self.image.copy()
            ghost.set_alpha(140)
            self.screen.blit(ghost, (self.rect.x - 80, self.rect.y))
            self.screen.blit(ghost, (self.rect.x + 80, self.rect.y))

        # Main ship
        self.screen.blit(self.image, self.rect)

        # Power-up glow ring
        if self.double_damage:
            pygame.draw.circle(self.screen, (255, 200, 0), self.rect.center, 38, 2)
        if self.rapid_fire:
            pygame.draw.circle(self.screen, (0, 200, 255), self.rect.center, 42, 2)

        # Explosion ring (W)
        if self.show_explosion:
            now = pygame.time.get_ticks()
            if now - self.explosion_start_time < self.ai_settings.explosion_visual_duration:
                elapsed = now - self.explosion_start_time
                ratio = elapsed / self.ai_settings.explosion_visual_duration
                radius = int(self.ai_settings.explosion_radius * ratio)
                alpha = int(255 * (1 - ratio))
                surf = pygame.Surface(
                    (radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 80, 0, alpha),
                                   (radius + 2, radius + 2), radius, 3)
                self.screen.blit(surf, (self.rect.centerx - radius - 2,
                                        self.rect.centery - radius - 2))
            else:
                self.show_explosion = False

        # Shield ring (Q)
        if self.has_shield:
            pygame.draw.circle(self.screen, (0, 255, 255), self.rect.center, 46, 2)
            pygame.draw.circle(self.screen, (0, 200, 200, 80), self.rect.center, 44, 8)
