import pygame
from random import randint

class StarField:
    """Scrolling starfield background."""

    def __init__(self, screen_width: int, screen_height: int, count: int = 120):
        self.w = screen_width
        self.h = screen_height
        self.stars = [
            [randint(0, screen_width), randint(0, screen_height),
             randint(1, 3)]   # size / speed layer
            for _ in range(count)
        ]

    def update_and_draw(self, screen: pygame.Surface) -> None:
        for star in self.stars:
            x, y, layer = star
            speed = layer * 0.4
            y += speed
            if y > self.h:
                y = 0
                x = randint(0, self.w)
            star[0], star[1] = x, y

            brightness = 100 + layer * 50
            blue = min(255, brightness + 30)
            size = layer
            pygame.draw.circle(screen, (brightness, brightness, blue),
                                (int(x), int(y)), size)
