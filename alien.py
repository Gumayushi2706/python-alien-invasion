import pygame
from pygame.sprite import Sprite
from random import choice

class Alien(Sprite):
    """A single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.hp = 1

        self.image = pygame.image.load('images/aliens.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = choice([1, -1])

    def check_edge(self) -> bool:
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self) -> None:
        self.x += self.ai_settings.alien_speed_factor * self.direction
        self.rect.x = self.x

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1

        self.y += self.ai_settings.alien_drop_speed
        self.rect.y = self.y

    def blitme(self) -> None:
        self.screen.blit(self.image, self.rect)


class BossAlien(Alien):
    """A tough boss alien that appears every N waves."""

    def __init__(self, ai_settings, screen):
        super(BossAlien, self).__init__(ai_settings, screen)
        self.hp = ai_settings.boss_hp
        self.max_hp = ai_settings.boss_hp

        # Load and scale bigger
        self.image_normal = pygame.image.load('images/aliens.png').convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (100, 100))
        self.image_hurt = self.image_normal.copy()
        # Tint hurt image red
        red_overlay = pygame.Surface((100, 100), pygame.SRCALPHA)
        red_overlay.fill((200, 0, 0, 100))
        self.image_hurt.blit(red_overlay, (0, 0))

        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def take_hit(self) -> bool:
        """Returns True if boss is dead."""
        self.hp -= 1
        if self.hp <= self.max_hp // 2:
            self.image = self.image_hurt
        return self.hp <= 0

    def draw_health_bar(self, screen) -> None:
        bar_width = 100
        bar_height = 8
        x = self.rect.x
        y = self.rect.y - 14
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (60, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (220, 50, 50), (x, y, int(bar_width * ratio), bar_height))
        pygame.draw.rect(screen, (255, 100, 100), (x, y, bar_width, bar_height), 1)
