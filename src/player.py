import arcade
from src.constants import *


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(str(IMAGES_DIR / "ship.png"), scale=1.0)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = GAME_ZONE_BOTTOM + 50
        self.hp = PLAYER_HP
        self.speed = PLAYER_SPEED
        self.heat = 0
        self.overheated = False
        self.super_shot_timer = SUPER_SHOT_COOLDOWN
        self.flash_timer = 0.0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        if self.heat > 0:
            self.heat -= 15 * delta_time  # Остывание
            if self.heat < 0: self.heat = 0

        if self.overheated and self.heat < 10:
            self.overheated = False

        if self.super_shot_timer < SUPER_SHOT_COOLDOWN:
            self.super_shot_timer += delta_time

        if self.color == (255, 0, 0):
            self.flash_timer -= delta_time
            if self.flash_timer <= 0:
                self.color = (255, 255, 255)

    def shoot(self):
        if self.overheated:
            return False
        self.heat += 15
        if self.heat >= 100:
            self.heat = 100
            self.overheated = True
        return True

    def reset_heat(self):
        self.heat = 0
        self.overheated = False