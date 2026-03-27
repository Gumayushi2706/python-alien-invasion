import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Bullet fired from the ship upward."""

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        self.image = pygame.image.load('images/bullets.png')
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self) -> None:
        self.y -= self.speed_factor
        self.rect.y = self.y

    def drawBullet(self) -> None:
        self.screen.blit(self.image, self.rect)


class AlienBullet(Sprite):
    """Bullet fired by an alien downward."""

    def __init__(self, ai_settings, screen, alien):
        super(AlienBullet, self).__init__()
        self.screen = screen
        self.speed = ai_settings.alien_bullet_speed

        # Draw a simple glowing red oval
        self.image = pygame.Surface((8, 18), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 60, 60, 220), (0, 0, 8, 18))
        pygame.draw.ellipse(self.image, (255, 180, 180, 120), (1, 1, 6, 16))

        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y += self.speed
        self.rect.y = self.y

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
