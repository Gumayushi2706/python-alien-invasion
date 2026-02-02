import sys
import pygame 
import math 
from bullet import Bullet
from alien import Alien  
from time import sleep 
from button import Button 
from random import randint 
def check_keydown(event, ai_settings, screen, ship, bullets, aliens, stats):
     current_time = pygame.time.get_ticks()
     if event.type == pygame.KEYDOWN: 
          if event.key == pygame.K_RIGHT:
               ship.moving_right = True 
          elif event.key == pygame.K_LEFT: 
               ship.moving_left =  True 
          elif event.key == pygame.K_UP: 
               ship.moving_up =  True
          elif event.key == pygame.K_DOWN: 
               ship.moving_down =  True
          elif event.key == pygame.K_SPACE:
               #Create a bullet and add it to a group 
               firingBullet(ai_settings, screen, ship, bullets)
          # --- Q: HP Shield------
          elif event.key == pygame.K_q:
               if current_time - ship.last_q > ai_settings.cd_q:
                    ship.has_shield = True
                    ship.last_q = current_time # Ghi lại thời gian dùng
          # --- W: Explosion
          elif event.key == pygame.K_w:
               if current_time - ship.last_w > ai_settings.cd_w:
            # 1. Gọi hàm logic nổ (xóa quái)
                    trigger_explosion(ai_settings, ship, aliens)
            # 2. Ghi nhận thời gian để tính hồi chiêu
                    ship.last_w = current_time
            # --- THÊM 2 DÒNG NÀY ĐỂ KÍCH HOẠT VISUAL ---
                    ship.show_explosion = True             # Bật công tắc vẽ
                    ship.explosion_start_time = current_time # Ghi lại thời điểm bắt đầu vẽ
            # -------------------------------------------
          # --- E: ---
          elif event.key == pygame.K_e:
               if current_time - ship.last_e > ai_settings.cd_e:
                    ship.is_cloned = True
                    ship.clone_start_time = current_time
                    ship.last_e = current_time
          # --- R: Destruction ---
          elif event.key == pygame.K_r:
               if current_time - ship.last_r > ai_settings.cd_r:
                    aliens.empty() # Xóa sạch quái
                    bullets.empty() # Xóa sạch đạn cho đỡ lag
                    stats.last_alien_spawn_time = current_time
                    ship.last_r = current_time
          elif event.key == pygame.K_ESCAPE: 
               sys.exit() 
# --- Helper function W ---
def trigger_explosion(ai_settings, ship, aliens):
    """Calculate the distance to erase aliens"""
    ship_center = ship.rect.center
    for alien in aliens.copy():
        alien_center = alien.rect.center
        # By Pythago 
        distance = math.hypot(ship_center[0] - alien_center[0], ship_center[1] - alien_center[1])
        
        if distance < ai_settings.explosion_radius:
            aliens.remove(alien) # Delete aliens in areas 
def firingBullet(ai_settings, screen, ship, bullets): 
     """Fire a bullet if limit not reached yet."""
     if len(bullets) < ai_settings.bullet_allowed: 
                    new_bullet = Bullet(ai_settings, screen, ship)
                    bullets.add(new_bullet) 
     if ship.is_cloned:
            left_bullet = Bullet(ai_settings, screen, ship)
            left_bullet.rect.x -= 100 # Dời sang trái
            bullets.add(left_bullet)

            right_bullet = Bullet(ai_settings, screen, ship)
            right_bullet.rect.x += 100 # Dời sang phải
            bullets.add(right_bullet)
def check_keyup(event, ship):
     if event.type == pygame.KEYUP: 
          if event.key == pygame.K_RIGHT:
               ship.moving_right = False 
          if event.key == pygame.K_LEFT: 
               ship.moving_left =  False 
          if event.key == pygame.K_UP: 
               ship.moving_up =  False 
          if event.key == pygame.K_DOWN: 
               ship.moving_down =  False 
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Watch for keyboard and mouse events"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_x, mouse_y = pygame.mouse.get_pos()
                 check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                 check_keydown(event, ai_settings, screen, ship, bullets, aliens, stats) 
            elif event.type == pygame.KEYUP: 
                 check_keyup(event, ship) 
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y): 
     """Start a new game when the player clicks Play."""
     button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
     if button_clicked and not stats.game_active:
          # Hide the mouse cursor.
          pygame.mouse.set_visible(False)
          stats.reset_stats()
          stats.game_active = True
          # Reset the game statistics.
          
          # Empty the list of aliens and bullets.
          aliens.empty()
          bullets.empty()
 
          # Create a new fleet and center the ship.
          #create_fleet(ai_settings, screen, ship, aliens)
          ship.center_ship()
          # Reset the scoreboard images.
          sb.prep_score()
          sb.prep_high_score()
          sb.prep_ships()
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
     """Respond to ship being hit by alien."""
     if ship.has_shield:
        ship.has_shield = False # No shield 
        # Đẩy lùi quái ra xa một chút để không bị dính damage tiếp ngay lập tức (Optional)
        aliens.empty() 
        create_fleet(ai_settings, screen, ship, aliens) # Hoặc reset quái
        return # Thoát hàm ngay, không trừ mạng
     if stats.ships_left > 0:
          # Decrement ships_left.
          stats.ships_left -= 1
          # Update scoreboard.
          sb.prep_ships()
          # Empty the list of aliens and bullets.
          aliens.empty()
          bullets.empty()
          # Create a new fleet and center the ship.
          #create_fleet(ai_settings, screen, ship, aliens)
          ship.center_ship()
          # Pause.
          sleep(0.5)
     else:    
          stats.game_active = False 
          pygame.mouse.set_visible(True)
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
     bullets.update()
        #Get rid of bullets that have disappear
     for bullet in bullets.copy(): 
          if bullet.rect.bottom <= 0:
               bullets.remove(bullet)
     # Check for any bullets that have hit aliens.
     # If so, get rid of the bullet and the alien.
     check_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
def check_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
     """Respond to bullet-alien collisions."""
     # Remove any bullets and aliens that have collided
     collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
     if collisions:
          for aliens in collisions.values():
               stats.score += ai_settings.alien_points * len(aliens)
               sb.prep_score()
          check_high_score(stats, sb) 
     if len(aliens) == 0:
     # Destroy existing bullets and create new fleet.
          bullets.empty()
          create_fleet(ai_settings, screen, ship, aliens)
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
     """Check if any aliens have reached the bottom of the screen."""
     screen_rect = screen.get_rect()
     for alien in aliens.sprites():
         if alien.rect.bottom >= screen_rect.bottom:
               # Treat this the same as if the ship got hit.
               ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
               break
def get_number_aliens_x(ai_settings, alien_width):
     """Determine the number of aliens that fit in a row."""
     available_space_x = ai_settings.screen_width - 3 * alien_width
     number_aliens_x = int(available_space_x / (3 * alien_width))
     return number_aliens_x 
def get_number_rows(ai_settings, ship_height, alien_height):
     """Determine the number of rows of aliens that fit on the screen."""
     available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
     number_rows = int(available_space_y / (3 * alien_height))
     return number_rows
def create_new_row(ai_settings, screen, aliens):
    """Only create a row on the top screen"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # Number aliens of a row 
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    
    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, aliens, alien_number, 0)
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
     alien = Alien(ai_settings, screen) 
     alien_width = alien.rect.width 
     alien.x = alien_width + 3*alien_width*alien_number
     alien.rect.x = alien.x 
     alien.rect.y = alien.rect.height + 3 * alien.rect.height * row_number
     aliens.add(alien)
def create_fleet(ai_settings, screen, ship, aliens): 
     """Create a full fleet of aliens."""
     alien = Alien(ai_settings, screen)
     number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
     number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height) 
     #Create the first row aliens
     for row_number in range(number_rows):
          for alien_number in range(number_aliens_x):
               #Create an alien and place it in a row
               create_alien(ai_settings, screen, aliens, alien_number, row_number)
def check_fleet_edges(ai_settings, aliens):
     """Respond appropriately if any aliens have reached an edge."""
     for alien in aliens.sprites():
          if alien.check_edge():
               change_fleet_direction(ai_settings, aliens)
               break
def change_fleet_direction(ai_settings, aliens):
     """Drop the entire fleet and change the fleet's direction."""
     for alien in aliens.sprites():
          alien.rect.y += ai_settings.fleet_drop_speed
     ai_settings.fleet_direction *= -1
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
     """Check if the fleet is at an edge, and then update the postions of all aliens in the fleet."""
     #check_fleet_edges(ai_settings, aliens)
     aliens.update() 
     # --- LOGIC MỚI: SINH QUÁI SAU 0.5 GIÂY ---
     current_time = pygame.time.get_ticks()
    
    # 500 là số mili giây (tức là 0.5 giây). 
    # Bạn có thể tăng lên 1000 hoặc 2000 nếu thấy quái ra quá đông.
     if current_time - stats.last_alien_spawn_time > 2000: 
        create_new_row(ai_settings, screen, aliens)
        stats.last_alien_spawn_time = current_time # Reset đồng hồ
    # -----------------------------------------
     # Look for alien-ship collisions.
     if pygame.sprite.spritecollideany(ship, aliens):
          ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
     # Look for aliens hitting the bottom of the screen.
     check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
def check_high_score(stats, sb):
     """Check to see if there's a new high score."""
     if stats.score > stats.high_score: 
          stats.high_score = stats.score
          sb.prep_high_score() 
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen.""" 
    #Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    #Redraw bullets behind ship and aliens 
    for bullet in bullets.sprites(): 
         bullet.drawBullet()
    ship.blitme()
    aliens.draw(screen) 
    # Draw the score information.
    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
          play_button.draw_button()
    #Make the most recently drawn screen visible.
    pygame.display.flip()
    
