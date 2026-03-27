import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button, GameOverScreen
from scoreboard import Scoreboard
from hud import HUD
from stars import StarField
import game_functions as gf


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Objects
    play_button      = Button(ai_settings, screen, "Play")
    stats            = GameStats(ai_settings)
    stats.show_game_over = False
    sb               = Scoreboard(ai_settings, screen, stats)
    hud              = HUD(screen, ai_settings, stats)
    game_over_screen = GameOverScreen(ai_settings, screen, stats)
    ship             = Ship(ai_settings, screen)
    stars            = StarField(ai_settings.screen_width, ai_settings.screen_height)

    # Sprite groups
    bullets       = Group()
    alien_bullets = Group()
    aliens        = Group()
    bosses        = Group()
    powerups      = Group()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        gf.check_events(
            ai_settings, screen, stats, sb, play_button,
            game_over_screen, ship, aliens, bosses,
            bullets, alien_bullets, powerups)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship,
                               aliens, bosses, bullets, alien_bullets, powerups)
            gf.update_alien_bullets(ai_settings, screen, stats, sb, ship,
                                     aliens, bosses, bullets, alien_bullets, powerups)
            gf.update_aliens(ai_settings, screen, stats, sb, ship,
                              aliens, bosses, bullets, alien_bullets, powerups)
            gf.update_powerups(ai_settings, screen, stats, sb, ship,
                                aliens, bosses, bullets, alien_bullets, powerups)

        gf.update_screen(
            ai_settings, screen, stats, sb, hud, ship,
            aliens, bosses, bullets, alien_bullets,
            powerups, play_button, game_over_screen, stars)


run_game()
