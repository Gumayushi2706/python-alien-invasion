class Settings():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Ship settings 
        self.ship_speed_factor = 1
        self.ship_limit = 2
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Bullet settings 
        self.bullet_speed_factor = 1
        
        self.bullet_allowed = 5
        #Alien settings 
        self.alien_speed_factor = 0.1 
        self.fleet_drop_speed = 0.25
        # Scoring
        self.alien_points = 50
        # How quickly the alien point values increase
        self.score_scale = 1.2 
        self.alien_points = int(self.alien_points * self.score_scale)
        # --- SKILL SETTINGS ---
        # (Cooldown) 
        self.cd_q = 400 # 10s (Q - Khiên)
        self.cd_w = 500   # 5s  (W - Nổ xung quanh)
        self.cd_e = 600  # 15s (E - Phân thân)
        self.cd_r = 1000  # 60s (R - Hủy diệt)
        # Details
        self.explosion_radius = 200  # Radius of W
        self.clone_duration = 5000   # Time of existance
        self.explosion_visual_duration = 200  
    