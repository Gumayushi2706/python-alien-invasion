import pygame 
from pygame.sprite import Sprite 
class Ship(Sprite): 
    def __init__(self, ai_settings, screen): 
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings 
        #Load the ship image and get its rect 
        self.image = pygame.image.load('images/ships.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ((50, 50)))
        self.rect = self.image.get_rect()
        self.screen_rect= self.screen.get_rect()
        #Start each new ship at the bottom center of screen 
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #Store a decimal value for the ship's center 
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Movement flag
        self.moving_right = False
        self.moving_left = False 
        self.moving_up = False 
        self.moving_down = False 
        # --- System of new skills ---
        # 1. The last time to use skills 
        self.last_q = 0
        self.last_w = 0
        self.last_e = 0
        self.last_r = 0

        # 2. State 
        self.has_shield = False      # Q: Có khiên hay không
        self.is_cloned = False       # E: Đang phân thân hay không
        self.clone_start_time = 0    # Thời điểm bắt đầu phân thân
        self.show_explosion = False      # Có đang hiện vòng tròn không?
        self.explosion_start_time = 0    # Thời điểm bắt đầu hiện
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centery = float(self.rect.centery)
    def update(self):
        """Update the ship's position based on the movement flag."""
        #Update the ship center value, not the rect 
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0: 
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor 
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        #Update rect object by self.center
        self.rect.centerx = self.center 
        self.rect.centery = self.centery
        if self.is_cloned:
            now = pygame.time.get_ticks()
            if now - self.clone_start_time > self.ai_settings.clone_duration:
                self.is_cloned = False 
    def blitme(self):
        """Draw the ship at its current location."""
        # 1. Vẽ phân thân (E) nếu đang kích hoạt
        if self.is_cloned:
            # Vẽ 2 tàu ảo bên trái và phải
            self.screen.blit(self.image, (self.rect.x - 100, self.rect.y))
            self.screen.blit(self.image, (self.rect.x + 100, self.rect.y))
        # 2. Vẽ tàu chính
        self.screen.blit(self.image, self.rect)
        # --- VẼ HIỆU ỨNG NỔ (W) ---
        if self.show_explosion:
            current_time = pygame.time.get_ticks()
            # Kiểm tra nếu vẫn còn trong thời gian hiển thị (ví dụ dưới 200ms từ lúc bấm)
            if current_time - self.explosion_start_time < self.ai_settings.explosion_visual_duration:
                # Vẽ vòng tròn: (Màn hình, Màu đỏ, Tâm, Bán kính, Độ dày viền)
                # Độ dày viền = 2 (nếu để 0 sẽ là hình tròn đặc)
                pygame.draw.circle(self.screen, (255, 0, 0), self.rect.center, self.ai_settings.explosion_radius, 2)
            else:
                # Hết giờ thì tắt trạng thái hiển thị đi
                self.show_explosion = False
        # 3. Vẽ vòng tròn bảo vệ (Q) nếu có khiên
        if self.has_shield:
            pygame.draw.circle(self.screen, (0, 255, 255), self.rect.center, 50, 2)

