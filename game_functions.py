"""
game_functions.py
Tách logic thành các nhóm rõ ràng:
  - Input handling  (check_events, check_keydown, check_keyup)
  - Skill actions   (trigger_explosion, firingBullet)
  - Spawning        (create_alien, create_new_row, create_fleet, spawn_boss)
  - Collisions      (check_collisions, check_alien_bullets_hit_ship)
  - Updates         (update_bullets, update_aliens, update_alien_bullets, update_powerups)
  - Rendering       (update_screen)
"""

import sys
import math
import pygame
from random import choice, randint
from time import sleep

from bullet import Bullet, AlienBullet
from alien import Alien, BossAlien
from powerup import maybe_drop
from button import GameOverScreen


# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------

def check_events(ai_settings, screen, stats, sb, play_button,
                 game_over_screen, ship, aliens, bosses,
                 bullets, alien_bullets, powerups):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if stats.game_active:
                pass
            elif stats.show_game_over:
                action = game_over_screen.check_click(mx, my)
                if action == 'play':
                    _start_game(ai_settings, screen, stats, sb,
                                ship, aliens, bosses, bullets, alien_bullets, powerups)
                elif action == 'quit':
                    sys.exit()
            else:
                if play_button.rect.collidepoint(mx, my):
                    _start_game(ai_settings, screen, stats, sb,
                                ship, aliens, bosses, bullets, alien_bullets, powerups)

        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, stats, sb,
                          ship, aliens, bosses, bullets, alien_bullets, powerups)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)


def check_keydown(event, ai_settings, screen, stats, sb,
                  ship, aliens, bosses, bullets, alien_bullets, powerups):
    now = pygame.time.get_ticks()
    k = event.key

    if k == pygame.K_RIGHT:  ship.moving_right = True
    elif k == pygame.K_LEFT:  ship.moving_left  = True
    elif k == pygame.K_UP:    ship.moving_up    = True
    elif k == pygame.K_DOWN:  ship.moving_down  = True
    elif k == pygame.K_ESCAPE: sys.exit()

    elif k == pygame.K_SPACE:
        if stats.game_active:
            firingBullet(ai_settings, screen, ship, bullets)

    # Q – Shield
    elif k == pygame.K_q:
        if stats.game_active and now - ship.last_q > ai_settings.cd_q:
            ship.has_shield = True
            ship.last_q = now

    # W – Explosion blast
    elif k == pygame.K_w:
        if stats.game_active and now - ship.last_w > ai_settings.cd_w:
            trigger_explosion(ai_settings, stats, sb, ship, aliens, bosses)
            ship.last_w = now
            ship.show_explosion = True
            ship.explosion_start_time = now

    # E – Clone
    elif k == pygame.K_e:
        if stats.game_active and now - ship.last_e > ai_settings.cd_e:
            ship.is_cloned = True
            ship.clone_start_time = now
            ship.last_e = now

    # R – Destroy all
    elif k == pygame.K_r:
        if stats.game_active and now - ship.last_r > ai_settings.cd_r:
            killed = len(aliens) + len(bosses)
            aliens.empty()
            bosses.empty()
            alien_bullets.empty()
            stats.score += ai_settings.alien_points * killed
            sb.prep_score()
            check_high_score(stats, sb)
            stats.last_alien_spawn_time = now
            ship.last_r = now
            _check_wave_clear(ai_settings, screen, stats, sb, ship,
                               aliens, bosses, bullets, alien_bullets, powerups)


def check_keyup(event, ship):
    k = event.key
    if k == pygame.K_RIGHT: ship.moving_right = False
    if k == pygame.K_LEFT:  ship.moving_left  = False
    if k == pygame.K_UP:    ship.moving_up    = False
    if k == pygame.K_DOWN:  ship.moving_down  = False


# ---------------------------------------------------------------------------
# Skill actions
# ---------------------------------------------------------------------------

def trigger_explosion(ai_settings, stats, sb, ship, aliens, bosses):
    center = ship.rect.center
    r = ai_settings.explosion_radius
    killed = 0

    for alien in aliens.copy():
        if math.hypot(center[0] - alien.rect.centerx,
                      center[1] - alien.rect.centery) < r:
            aliens.remove(alien)
            killed += 1

    for boss in bosses.copy():
        if math.hypot(center[0] - boss.rect.centerx,
                      center[1] - boss.rect.centery) < r:
            if boss.take_hit():
                bosses.remove(boss)
                stats.score += ai_settings.boss_points
                killed += 1

    stats.score += ai_settings.alien_points * killed
    stats.aliens_killed_this_wave += killed
    if killed:
        sb.prep_score()
        check_high_score(stats, sb)


def firingBullet(ai_settings, screen, ship, bullets):
    limit = (ai_settings.rapid_fire_allowed
             if ship.rapid_fire else ai_settings.bullet_allowed)

    if len(bullets) < limit:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

        # Clone side-bullets (only when cloned is active)
        if ship.is_cloned:
            left_b = Bullet(ai_settings, screen, ship)
            left_b.rect.x -= 80
            left_b.x = float(left_b.rect.x)
            bullets.add(left_b)

            right_b = Bullet(ai_settings, screen, ship)
            right_b.rect.x += 80
            right_b.x = float(right_b.rect.x)
            bullets.add(right_b)


# ---------------------------------------------------------------------------
# Spawning
# ---------------------------------------------------------------------------

def get_number_aliens_x(ai_settings, alien_width: int) -> int:
    available = ai_settings.screen_width - 3 * alien_width
    return int(available / (3 * alien_width))


def create_alien(ai_settings, screen, aliens, alien_number: int, row_number: int = 0):
    alien = Alien(ai_settings, screen)
    w = alien.rect.width
    alien.x = w + 3 * w * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 3 * alien.rect.height * row_number
    aliens.add(alien)


def create_new_row(ai_settings, screen, aliens):
    tmp = Alien(ai_settings, screen)
    n = get_number_aliens_x(ai_settings, tmp.rect.width)
    for i in range(n):
        create_alien(ai_settings, screen, aliens, i, 0)


def create_fleet(ai_settings, screen, ship, aliens):
    tmp = Alien(ai_settings, screen)
    nx = get_number_aliens_x(ai_settings, tmp.rect.width)
    available_y = (ai_settings.screen_height - 3 * tmp.rect.height - ship.rect.height)
    nr = int(available_y / (3 * tmp.rect.height))
    for row in range(nr):
        for col in range(nx):
            create_alien(ai_settings, screen, aliens, col, row)


def spawn_boss(ai_settings, screen, bosses):
    boss = BossAlien(ai_settings, screen)
    boss.x = ai_settings.screen_width // 2 - boss.rect.width // 2
    boss.rect.x = boss.x
    boss.rect.y = 20
    boss.y = float(boss.rect.y)
    bosses.add(boss)


# ---------------------------------------------------------------------------
# Ship hit / game over
# ---------------------------------------------------------------------------

def ship_hit(ai_settings, screen, stats, sb, ship,
             aliens, bosses, bullets, alien_bullets, powerups):
    if ship.has_shield:
        ship.has_shield = False
        aliens.empty()
        alien_bullets.empty()
        create_new_row(ai_settings, screen, aliens)
        return

    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bosses.empty()
        bullets.empty()
        alien_bullets.empty()
        powerups.empty()
        ship.center_ship()
        sleep(0.4)
    else:
        stats.game_active = False
        stats.show_game_over = True
        pygame.mouse.set_visible(True)


# ---------------------------------------------------------------------------
# Collisions
# ---------------------------------------------------------------------------

def check_collisions(ai_settings, screen, stats, sb, ship,
                     aliens, bosses, bullets, alien_bullets, powerups):
    # Player bullets vs normal aliens
    hits = pygame.sprite.groupcollide(bullets, aliens, True, False)
    for bullet, hit_aliens in hits.items():
        for alien in hit_aliens:
            damage = 2 if ship.double_damage else 1
            alien.hp -= damage
            if alien.hp <= 0:
                drop = maybe_drop(screen, ai_settings, alien)
                if drop:
                    powerups.add(drop)
                aliens.remove(alien)
                stats.score += ai_settings.alien_points
                stats.aliens_killed_this_wave += 1
        sb.prep_score()
    check_high_score(stats, sb)

    # Player bullets vs boss
    boss_hits = pygame.sprite.groupcollide(bullets, bosses, True, False)
    for bullet, hit_bosses in boss_hits.items():
        for boss in hit_bosses:
            damage = 2 if ship.double_damage else 1
            for _ in range(damage):
                if boss.take_hit():
                    bosses.remove(boss)
                    stats.score += ai_settings.boss_points
                    stats.aliens_killed_this_wave += 3
                    break
        sb.prep_score()
    check_high_score(stats, sb)


def check_alien_bullets_hit_ship(ai_settings, screen, stats, sb, ship,
                                  aliens, bosses, bullets, alien_bullets, powerups):
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        # Remove the bullet that hit
        for ab in alien_bullets.copy():
            if ab.rect.colliderect(ship.rect):
                alien_bullets.remove(ab)
                break
        ship_hit(ai_settings, screen, stats, sb, ship,
                 aliens, bosses, bullets, alien_bullets, powerups)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship,
                         aliens, bosses, bullets, alien_bullets, powerups):
    bottom = screen.get_rect().bottom
    for alien in aliens.sprites():
        if alien.rect.bottom >= bottom:
            ship_hit(ai_settings, screen, stats, sb, ship,
                     aliens, bosses, bullets, alien_bullets, powerups)
            break
    for boss in bosses.sprites():
        if boss.rect.bottom >= bottom:
            ship_hit(ai_settings, screen, stats, sb, ship,
                     aliens, bosses, bullets, alien_bullets, powerups)
            break


# ---------------------------------------------------------------------------
# Wave progression
# ---------------------------------------------------------------------------

def _check_wave_clear(ai_settings, screen, stats, sb, ship,
                       aliens, bosses, bullets, alien_bullets, powerups):
    if len(aliens) == 0 and len(bosses) == 0:
        bullets.empty()
        alien_bullets.empty()
        powerups.empty()
        stats.wave += 1
        stats.aliens_killed_this_wave = 0
        ai_settings.scale_for_wave(stats.wave)
        sb.prep_score()

        if stats.wave % ai_settings.boss_wave_interval == 0:
            spawn_boss(ai_settings, screen, bosses)
        else:
            create_new_row(ai_settings, screen, aliens)

        stats.last_alien_spawn_time = pygame.time.get_ticks()


# ---------------------------------------------------------------------------
# Update loops
# ---------------------------------------------------------------------------

def update_bullets(ai_settings, screen, stats, sb, ship,
                   aliens, bosses, bullets, alien_bullets, powerups):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_collisions(ai_settings, screen, stats, sb, ship,
                     aliens, bosses, bullets, alien_bullets, powerups)
    _check_wave_clear(ai_settings, screen, stats, sb, ship,
                       aliens, bosses, bullets, alien_bullets, powerups)


def update_alien_bullets(ai_settings, screen, stats, sb, ship,
                          aliens, bosses, bullets, alien_bullets, powerups):
    alien_bullets.update()
    for ab in alien_bullets.copy():
        if ab.rect.top > ai_settings.screen_height:
            alien_bullets.remove(ab)

    check_alien_bullets_hit_ship(ai_settings, screen, stats, sb, ship,
                                  aliens, bosses, bullets, alien_bullets, powerups)

    # Aliens randomly shoot
    now = pygame.time.get_ticks()
    if (now - stats.last_alien_bullet_time > ai_settings.alien_bullet_cooldown
            and len(aliens) + len(bosses) > 0):
        all_enemies = aliens.sprites() + bosses.sprites()
        shooter = choice(all_enemies)
        alien_bullets.add(AlienBullet(ai_settings, screen, shooter))
        stats.last_alien_bullet_time = now


def update_aliens(ai_settings, screen, stats, sb, ship,
                  aliens, bosses, bullets, alien_bullets, powerups):
    aliens.update()
    bosses.update()

    now = pygame.time.get_ticks()
    if now - stats.last_alien_spawn_time > ai_settings.spawn_cooldown:
        if len(bosses) == 0:   # Don't spawn rows during boss fight
            create_new_row(ai_settings, screen, aliens)
        stats.last_alien_spawn_time = now

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship,
                 aliens, bosses, bullets, alien_bullets, powerups)
    if pygame.sprite.spritecollideany(ship, bosses):
        ship_hit(ai_settings, screen, stats, sb, ship,
                 aliens, bosses, bullets, alien_bullets, powerups)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship,
                         aliens, bosses, bullets, alien_bullets, powerups)


def update_powerups(ai_settings, screen, stats, sb, ship,
                    aliens, bosses, bullets, alien_bullets, powerups):
    powerups.update()
    for pu in powerups.copy():
        if pu.rect.top > ai_settings.screen_height:
            powerups.remove(pu)
            continue
        if pu.rect.colliderect(ship.rect):
            powerups.remove(pu)
            if pu.kind == 'hp':
                if stats.ships_left < ai_settings.ship_limit:
                    stats.ships_left += 1
                    sb.prep_ships()
            else:
                ship.apply_powerup(pu.kind)


# ---------------------------------------------------------------------------
# High score
# ---------------------------------------------------------------------------

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


# ---------------------------------------------------------------------------
# Start game helper
# ---------------------------------------------------------------------------

def _start_game(ai_settings, screen, stats, sb,
                ship, aliens, bosses, bullets, alien_bullets, powerups):
    pygame.mouse.set_visible(False)
    ai_settings._load_from_file()          # Reset settings to base
    stats.reset_stats()
    stats.game_active = True
    stats.show_game_over = False

    aliens.empty()
    bosses.empty()
    bullets.empty()
    alien_bullets.empty()
    powerups.empty()

    ship.center_ship()
    ship.has_shield = False
    ship.is_cloned = False
    ship.double_damage = False
    ship.rapid_fire = False

    create_new_row(ai_settings, screen, aliens)
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_ships()


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def update_screen(ai_settings, screen, stats, sb, hud, ship,
                  aliens, bosses, bullets, alien_bullets,
                  powerups, play_button, game_over_screen, stars):
    # Background
    screen.fill(ai_settings.bg_color)
    stars.update_and_draw(screen)

    # Bullets
    for bullet in bullets.sprites():
        bullet.drawBullet()
    for ab in alien_bullets.sprites():
        ab.draw()

    # Power-ups
    powerups.draw(screen)

    # Aliens
    aliens.draw(screen)

    # Bosses + health bars
    for boss in bosses.sprites():
        screen.blit(boss.image, boss.rect)
        boss.draw_health_bar(screen)

    # Ship
    ship.blitme()

    # HUD (score, hearts, wave, skills)
    sb.show_score()
    if stats.game_active:
        hud.draw(ship)

    # Screens
    if not stats.game_active:
        if stats.show_game_over:
            game_over_screen.draw()
        else:
            play_button.draw_button()

    pygame.display.flip()
