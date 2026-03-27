import json
import os

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        self._load_from_file()

    def _load_from_file(self):
        defaults = self._get_defaults()
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r') as f:
                    user = json.load(f)
                defaults.update(user)
            except Exception:
                pass
        for k, v in defaults.items():
            setattr(self, k, v)

    def _get_defaults(self) -> dict:
        return {
            # Screen
            'screen_width': 1200,
            'screen_height': 800,
            'bg_color': (10, 10, 20),

            # Ship
            'ship_speed_factor': 3,
            'ship_limit': 3,

            # Bullet
            'bullet_speed_factor': 8,
            'bullet_allowed': 5,

            # Alien base
            'alien_speed_factor': 0.8,
            'alien_drop_speed': 0.3,
            'fleet_drop_speed': 10,
            'fleet_direction': 1,

            # Scoring
            'alien_points': 50,
            'boss_points': 500,
            'score_scale': 1.5,

            # Wave / difficulty
            'spawn_cooldown': 2000,
            'speed_scale_per_wave': 0.12,
            'spawn_scale_per_wave': 0.9,
            'min_spawn_cooldown': 600,

            # Boss
            'boss_hp': 5,
            'boss_wave_interval': 5,

            # Skill cooldowns (ms)
            'cd_q': 8000,
            'cd_w': 5000,
            'cd_e': 8000,
            'cd_r': 20000,

            # Skill details
            'explosion_radius': 200,
            'clone_duration': 5000,
            'explosion_visual_duration': 300,

            # Alien bullet
            'alien_bullet_cooldown': 1500,
            'alien_bullet_speed': 3,

            # Power-up
            'powerup_drop_chance': 0.2,
            'powerup_speed': 2,
            'double_damage_duration': 10000,
            'rapid_fire_duration': 5000,
            'rapid_fire_allowed': 10,
        }

    def scale_for_wave(self, wave: int) -> None:
        """Increase difficulty each wave."""
        factor = wave - 1
        base = self._get_defaults()
        self.alien_speed_factor = base['alien_speed_factor'] * (
            1 + self.speed_scale_per_wave * factor)
        self.spawn_cooldown = max(
            self.min_spawn_cooldown,
            int(base['spawn_cooldown'] * (self.spawn_scale_per_wave ** factor))
        )
        self.alien_bullet_cooldown = max(
            600,
            int(base['alien_bullet_cooldown'] * (0.92 ** factor))
        )
