import pygame
from pygame.sprite import Group
from hearts import Heart

class Scoreboard():
    """Reports scoring information on screen."""

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (200, 200, 220)
        self.font = pygame.font.SysFont(None, 42)
        self.small_font = pygame.font.SysFont(None, 26)

        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_score(self) -> None:
        rounded = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self) -> None:
        high = int(round(self.stats.high_score, -1))
        hs_str = "BEST  {:,}".format(high)
        self.high_score_image = self.small_font.render(hs_str, True, (140, 140, 180))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 36

    def prep_ships(self) -> None:
        self.ships = Group()
        for i in range(self.stats.ships_left):
            heart = Heart(self.screen)
            heart.rect.x = 10 + i * (heart.rect.width + 4)
            heart.rect.y = 10
            self.ships.add(heart)

    def show_score(self) -> None:
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)
