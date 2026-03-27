import pygame

SKILL_KEYS   = ['Q', 'W', 'E', 'R']
SKILL_COLORS = [
    (0,   220, 220),   # Q – cyan   (shield)
    (255,  80,  40),   # W – orange (explosion)
    (60,  200,  80),   # E – green  (clone)
    (160,  60, 240),   # R – purple (destroy all)
]
SKILL_NAMES = ['Shield', 'Blast', 'Clone', 'Nuke']

class HUD:
    """Renders skill cooldown bars, wave number, and active power-up icons."""

    def __init__(self, screen, ai_settings, stats):
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        self.font_big   = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 20)

    def _cooldown_ratio(self, last_used: int, cooldown: int) -> float:
        """0.0 = on cooldown (just used), 1.0 = ready."""
        now = pygame.time.get_ticks()
        elapsed = now - last_used
        return min(1.0, elapsed / cooldown)

    def draw(self, ship) -> None:
        self._draw_skill_bar(ship)
        self._draw_wave_banner()
        self._draw_powerup_timers(ship)

    def _draw_skill_bar(self, ship) -> None:
        box_w, box_h = 52, 52
        gap = 8
        total_w = 4 * box_w + 3 * gap
        sx = (self.screen.get_width() - total_w) // 2
        sy = self.screen.get_height() - box_h - 12

        last_used = [ship.last_q, ship.last_w, ship.last_e, ship.last_r]
        cooldowns  = [self.ai_settings.cd_q, self.ai_settings.cd_w,
                      self.ai_settings.cd_e, self.ai_settings.cd_r]

        for i, (key, color, name) in enumerate(zip(SKILL_KEYS, SKILL_COLORS, SKILL_NAMES)):
            x = sx + i * (box_w + gap)
            ratio = self._cooldown_ratio(last_used[i], cooldowns[i])
            ready = ratio >= 1.0

            # Background
            pygame.draw.rect(self.screen, (20, 20, 35), (x, sy, box_w, box_h), border_radius=6)

            # Fill bar (bottom to top)
            if ratio > 0:
                fill_h = int(box_h * ratio)
                fill_color = color if ready else tuple(c // 3 for c in color)
                pygame.draw.rect(self.screen, fill_color,
                                 (x, sy + box_h - fill_h, box_w, fill_h),
                                 border_radius=6)

            # Border
            border_color = color if ready else (60, 60, 80)
            pygame.draw.rect(self.screen, border_color, (x, sy, box_w, box_h), 2, border_radius=6)

            # Key label
            key_surf = self.font_big.render(key, True,
                                            (255, 255, 255) if ready else (120, 120, 140))
            self.screen.blit(key_surf, (x + box_w // 2 - key_surf.get_width() // 2,
                                        sy + 8))

            # Skill name
            name_surf = self.font_small.render(name, True,
                                               (200, 200, 200) if ready else (80, 80, 100))
            self.screen.blit(name_surf, (x + box_w // 2 - name_surf.get_width() // 2,
                                         sy + 32))

            # Cooldown seconds remaining
            if not ready:
                remaining = cooldowns[i] - (pygame.time.get_ticks() - last_used[i])
                cd_str = f"{remaining / 1000:.1f}s"
                cd_surf = self.font_small.render(cd_str, True, (200, 200, 200))
                # Overlay centered
                overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                self.screen.blit(overlay, (x, sy))
                self.screen.blit(cd_surf, (x + box_w // 2 - cd_surf.get_width() // 2,
                                            sy + box_h // 2 - cd_surf.get_height() // 2))

    def _draw_wave_banner(self) -> None:
        wave_str = f"WAVE  {self.stats.wave}"
        surf = self.font_big.render(wave_str, True, (180, 180, 220))
        x = self.screen.get_width() // 2 - surf.get_width() // 2
        self.screen.blit(surf, (x, 10))

    def _draw_powerup_timers(self, ship) -> None:
        now = pygame.time.get_ticks()
        y = 60
        if ship.double_damage:
            rem = max(0, ship.double_damage_end - now) / 1000
            self._draw_powerup_tag(f"2x DMG  {rem:.1f}s", (255, 200, 0), y)
            y += 28
        if ship.rapid_fire:
            rem = max(0, ship.rapid_fire_end - now) / 1000
            self._draw_powerup_tag(f"RAPID  {rem:.1f}s", (0, 200, 255), y)

    def _draw_powerup_tag(self, text: str, color: tuple, y: int) -> None:
        surf = self.font_small.render(text, True, color)
        x = self.screen.get_width() - surf.get_width() - 16
        self.screen.blit(surf, (x, y))
