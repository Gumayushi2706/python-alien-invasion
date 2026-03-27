import pygame

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.high_score = 0
        self.reset_stats()
        self.game_active = False
        self.last_alien_spawn_time = pygame.time.get_ticks()
        self.last_alien_bullet_time = pygame.time.get_ticks()

    def reset_stats(self) -> None:
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.wave = 1
        self.aliens_killed_this_wave = 0
        self.aliens_per_wave = 12  # kill this many to advance wave
        self.last_alien_spawn_time = pygame.time.get_ticks()
        self.last_alien_bullet_time = pygame.time.get_ticks()
