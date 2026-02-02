import pygame 
from pygame.sprite import Sprite 
from random import choice 
class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings 
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/aliens.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,((50, 50)))
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = choice([1, -1])
    def check_edge(self): 
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True 
        elif self.rect.left <= 0: 
            return True   
    def update(self):
        """Move the alien right"""
        """self.x += (self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction) 
        self.rect.x = self.x""" 
        """Quái di chuyển zigzag và rơi xuống."""
        
        # 1. DI CHUYỂN NGANG
        # Tốc độ ngang = tốc độ cài đặt * hướng đi
        self.x += (self.ai_settings.alien_speed_factor * self.direction)
        self.rect.x = self.x
        
        # 2. KIỂM TRA ĐỤNG TƯỜNG (Để đổi hướng)
        screen_rect = self.screen.get_rect()
        
        # Nếu đụng cạnh phải
        if self.rect.right >= screen_rect.right:
            self.direction = -1 # Đổi hướng sang trái
            
        # Nếu đụng cạnh trái
        elif self.rect.left <= 0:
            self.direction = 1  # Đổi hướng sang phải
            
        # 3. DI CHUYỂN DỌC (Rơi xuống)
        # Bạn có thể nhân thêm số (vd: * 0.5) nếu muốn rơi chậm hơn đi ngang
        self.y += self.ai_settings.alien_speed_factor 
        self.rect.y = self.y
    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
