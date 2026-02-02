import pygame
from pygame.sprite import Sprite 

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__() 
        self.screen = screen 
        #Create a bullet rect at (0,0) and then set the correct position. 
        self.image = pygame.image.load('images/bullets.png')
        self.image = pygame.transform.scale(self.image, (10, 20)) 
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx 
        self.rect.top = ship.rect.top
        #Store the bullet's postion as a decimal value 
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor 
    def update(self):
        """Move the bullet up the screen"""
        #Update postion 
        self.y -= self.speed_factor
        self.rect.y =  self.y 
    def drawBullet(self):
        self.screen.blit(self.image, self.rect)
    

