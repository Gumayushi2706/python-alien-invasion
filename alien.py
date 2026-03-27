import pygame
from pygame.sprite import Sprite
from random import choice, randint
import math

# ---------------------------------------------------------------------------
# Alien type definitions
# ---------------------------------------------------------------------------
# Each entry: (tên, speed_mult, drop_mult, hp, points, color_tint, behavior)
# behavior: 'zigzag' | 'straight' | 'sine' | 'dive' | 'fast'
ALIEN_TYPES = [
    # name,       spd,  drop,  hp, pts, tint_rgb,          behavior
    ('Normal',    1.0,  1.0,   1,  50,  None,              'zigzag'),
    ('Speedy',    2.2,  0.5,   1,  80,  (100, 220, 255),   'fast'),
    ('Tank',      0.5,  0.6,   3,  150, (180, 80,  80),    'straight'),
    ('Sine',      1.2,  0.8,   1,  100, (80,  255, 160),   'sine'),
    ('Diver',     1.5,  1.5,   1,  120, (255, 180, 50),    'dive'),
    ('Ghost',     1.0,  0.5,   1,  90,  (180, 100, 255),   'zigzag'),
]

# Wave → which types can appear (index into ALIEN_TYPES)
def types_for_wave(wave: int) -> list:
    if wave <= 1:  return [0]
    if wave <= 2:  return [0, 1]
    if wave <= 3:  return [0, 1, 2]
    if wave <= 4:  return [0, 1, 2, 3]
    if wave <= 5:  return [0, 1, 2, 3, 4]
    return list(range(len(ALIEN_TYPES)))   # all types from wave 6+


class Alien(Sprite):
    """A single alien. Type is chosen based on the current wave."""

    def __init__(self, ai_settings, screen, wave: int = 1):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Pick type
        pool = types_for_wave(wave)
        type_idx = choice(pool)
        (self.type_name, spd_mult, drop_mult,
         self.hp, self.points, self.tint, self.behavior) = ALIEN_TYPES[type_idx]
        self.max_hp = self.hp

        # Speed / drop for this instance
        self.speed      = ai_settings.alien_speed_factor * spd_mult
        self.drop_speed = ai_settings.alien_drop_speed   * drop_mult

        # Sine wave state
        self._sine_t   = randint(0, 628) / 100.0  # random phase
        self._sine_amp = 60   # pixels

        # Dive state
        self._diving   = False
        self._dive_timer = randint(60, 180)  # frames before first dive

        # Load + tint image
        base = pygame.image.load('images/aliens.png').convert_alpha()
        base = pygame.transform.scale(base, (50, 50))
        if self.tint:
            tinted = base.copy()
            tinted.fill((*self.tint, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = tinted
        else:
            self.image = base

        # Ghost: semi-transparent
        if self.behavior == 'ghost':
            self.image.set_alpha(140)

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = choice([1, -1])

    # ------------------------------------------------------------------
    def update(self) -> None:
        screen_rect = self.screen.get_rect()

        if self.behavior == 'zigzag' or self.behavior == 'ghost':
            self._move_zigzag(screen_rect)

        elif self.behavior == 'fast':
            self._move_zigzag(screen_rect)   # same as zigzag but faster

        elif self.behavior == 'straight':
            # Just fall straight down, slow
            self.y += self.drop_speed
            self.rect.y = self.y

        elif self.behavior == 'sine':
            self._sine_t += 0.06
            self.x += self.speed * self.direction
            # Bounce walls
            if self.rect.right >= screen_rect.right or self.rect.left <= 0:
                self.direction *= -1
            # Sine vertical oscillation (stays mostly in row)
            self.rect.x = self.x
            base_y = self.y
            self.rect.y = int(base_y + math.sin(self._sine_t) * self._sine_amp)
            self.y += self.drop_speed * 0.4   # drift down slowly

        elif self.behavior == 'dive':
            self._dive_timer -= 1
            if self._dive_timer <= 0:
                self._diving = True
            if self._diving:
                # Plunge fast toward bottom
                self.y += self.drop_speed * 4
                self.rect.y = self.y
                if self.rect.top > screen_rect.bottom:
                    self.kill()   # off screen → remove
            else:
                self._move_zigzag(screen_rect)

    def _move_zigzag(self, screen_rect) -> None:
        self.x += self.speed * self.direction
        self.rect.x = self.x
        if self.rect.right >= screen_rect.right:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1
        self.y += self.drop_speed
        self.rect.y = self.y

    # ------------------------------------------------------------------
    def take_hit(self, damage: int = 1) -> bool:
        """Returns True if alien is dead."""
        self.hp -= damage
        # Flash red on hit for tank
        if self.max_hp > 1 and self.hp > 0:
            pass  # health bar shows the state
        return self.hp <= 0

    def draw_health_bar(self, screen) -> None:
        """Only drawn for multi-HP aliens (Tank)."""
        if self.max_hp <= 1:
            return
        bar_w, bar_h = 44, 5
        x = self.rect.x + 3
        y = self.rect.y - 9
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (60, 0, 0),   (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, (200, 60, 60), (x, y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(screen, (255, 120, 120), (x, y, bar_w, bar_h), 1)

    def blitme(self) -> None:
        self.screen.blit(self.image, self.rect)


# ---------------------------------------------------------------------------
# Boss
# ---------------------------------------------------------------------------
class BossAlien(Alien):
    """Tough boss that appears every N waves."""

    def __init__(self, ai_settings, screen):
        # Don't call Alien.__init__ because we set everything manually
        Sprite.__init__(self)
        self.screen       = screen
        self.ai_settings  = ai_settings
        self.type_name    = 'Boss'
        self.hp           = ai_settings.boss_hp
        self.max_hp       = ai_settings.boss_hp
        self.points       = ai_settings.boss_points
        self.behavior     = 'zigzag'
        self.tint         = None
        self.speed        = ai_settings.alien_speed_factor * 1.4
        self.drop_speed   = ai_settings.alien_drop_speed   * 0.4
        self.direction    = 1
        self._sine_t      = 0.0
        self._sine_amp    = 0
        self._diving      = False
        self._dive_timer  = 9999

        base = pygame.image.load('images/aliens.png').convert_alpha()
        self.image_normal = pygame.transform.scale(base, (100, 100))
        hurt = self.image_normal.copy()
        hurt.fill((200, 0, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
        self.image_hurt = hurt
        self.image = self.image_normal

        self.rect  = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 20
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def take_hit(self, damage: int = 1) -> bool:
        self.hp -= damage
        self.image = self.image_hurt if self.hp <= self.max_hp // 2 else self.image_normal
        return self.hp <= 0

    def draw_health_bar(self, screen) -> None:
        bar_w, bar_h = 100, 8
        x, y = self.rect.x, self.rect.y - 14
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (60, 0, 0),   (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, (220, 50, 50), (x, y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(screen, (255, 100, 100), (x, y, bar_w, bar_h), 1)
