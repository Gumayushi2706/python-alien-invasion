import pygame
from pygame.sprite import Sprite

class Heart(Sprite):
    """A class to manage the heart image (representing lives left)."""
    def __init__(self, screen):
        """Initialize the heart and set its starting attributes."""
        super(Heart, self).__init__()
        self.screen = screen

        # Load the heart image from the images directory.
        # Note: Ensure you have 'heart.png' in the 'images' folder.
        self.image = pygame.image.load('images/hearts.png').convert_alpha()
        # Scale the image to 30x30 pixels.
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Get the image rect to handle positioning.
        self.rect = self.image.get_rect()