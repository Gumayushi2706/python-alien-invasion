import pygame
from pygame.sprite import Sprite
from random import choice, random

POWERUP_TYPES = ['hp', 'double_damage', 'rapid_fire']

COLORS = {
    'hp':            (50, 220, 100),
    'double_damage': (255, 180, 0),
    'rapid_fire':    (0, 180, 255),
}

LABELS = {
    'hp':            '+HP',
    'double_damage': '2x',
    'rapid_fire':    'RFR',
}


class PowerUp(Sprite):
    """A power-up item that drops from a dead alien."""

    def __init__(self, screen, ai_settings, x: int, y: int, kind: str = None):
        super(PowerUp, self).__init__()
        self.screen = screen
        self.speed = ai_settings.powerup_speed
        self.kind = kind if kind else choice(POWERUP_TYPES)

        color = COLORS[self.kind]
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (*color, 200), (0, 0, 36, 36), border_radius=6)
        pygame.draw.rect(self.image, (255, 255, 255, 180), (0, 0, 36, 36), 2, border_radius=6)

        font = pygame.font.SysFont(None, 18)
        label = font.render(LABELS[self.kind], True, (255, 255, 255))
        lx = (36 - label.get_width()) // 2
        ly = (36 - label.get_height()) // 2
        self.image.blit(label, (lx, ly))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y += self.speed
        self.rect.y = self.y

    def is_off_screen(self, screen_height: int) -> bool:
        return self.rect.top > screen_height


def maybe_drop(screen, ai_settings, alien) -> 'PowerUp | None':
    """Return a PowerUp with drop_chance probability, else None."""
    if random() < ai_settings.powerup_drop_chance:
        return PowerUp(screen, ai_settings, alien.rect.centerx, alien.rect.y)
    return None
