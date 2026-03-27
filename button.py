import pygame

class Button():
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 220, 56
        self.button_color = (30, 160, 90)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 52)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg: str) -> None:
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (80, 220, 130), self.rect, 2, border_radius=10)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class GameOverScreen():
    """Full Game Over overlay with score summary."""

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.font_title  = pygame.font.SysFont(None, 100)
        self.font_medium = pygame.font.SysFont(None, 52)
        self.font_small  = pygame.font.SysFont(None, 36)

        cx = self.screen_rect.centerx
        cy = self.screen_rect.centery

        # Play Again button
        self.play_rect = pygame.Rect(0, 0, 220, 56)
        self.play_rect.centerx = cx
        self.play_rect.y = cy + 80

        # Quit button
        self.quit_rect = pygame.Rect(0, 0, 160, 48)
        self.quit_rect.centerx = cx
        self.quit_rect.y = cy + 152

    def draw(self) -> None:
        # Dark overlay
        overlay = pygame.Surface(
            (self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 15, 200))
        self.screen.blit(overlay, (0, 0))

        cx = self.screen_rect.centerx
        cy = self.screen_rect.centery

        # GAME OVER title
        title = self.font_title.render("GAME OVER", True, (220, 50, 50))
        self.screen.blit(title, (cx - title.get_width() // 2, cy - 160))

        # Score
        score_str = "Score:  {:,}".format(int(round(self.stats.score, -1)))
        score_surf = self.font_medium.render(score_str, True, (220, 220, 255))
        self.screen.blit(score_surf, (cx - score_surf.get_width() // 2, cy - 40))

        # High score
        hs_str = "Best:   {:,}".format(int(round(self.stats.high_score, -1)))
        hs_surf = self.font_small.render(hs_str, True, (140, 140, 200))
        self.screen.blit(hs_surf, (cx - hs_surf.get_width() // 2, cy + 20))

        # Wave reached
        wave_str = f"Wave reached:  {self.stats.wave}"
        wave_surf = self.font_small.render(wave_str, True, (140, 200, 140))
        self.screen.blit(wave_surf, (cx - wave_surf.get_width() // 2, cy + 52))

        # Play Again button
        pygame.draw.rect(self.screen, (30, 160, 90), self.play_rect, border_radius=10)
        pygame.draw.rect(self.screen, (80, 220, 130), self.play_rect, 2, border_radius=10)
        play_label = self.font_small.render("Play Again", True, (255, 255, 255))
        self.screen.blit(play_label,
                         (cx - play_label.get_width() // 2,
                          self.play_rect.centery - play_label.get_height() // 2))

        # Quit button
        pygame.draw.rect(self.screen, (120, 30, 30), self.quit_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 60, 60), self.quit_rect, 2, border_radius=8)
        quit_label = self.font_small.render("Quit", True, (255, 200, 200))
        self.screen.blit(quit_label,
                         (cx - quit_label.get_width() // 2,
                          self.quit_rect.centery - quit_label.get_height() // 2))

    def check_click(self, mx: int, my: int) -> str:
        """Returns 'play', 'quit', or '' """
        if self.play_rect.collidepoint(mx, my):
            return 'play'
        if self.quit_rect.collidepoint(mx, my):
            return 'quit'
        return ''
