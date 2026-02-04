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

    def update(self, delta_time: float = 1 / 60):
        # Движение
        self.center_x += self.change_x

        # Ограничение движения границами экрана
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        # Остывание оружия
        if self.heat > 0:
            self.heat -= 15 * delta_time  # COOLING_RATE
            if self.heat < 0: self.heat = 0

        if self.overheated and self.heat < 10:
            self.overheated = False

        if self.super_shot_timer < SUPER_SHOT_COOLDOWN:
            self.super_shot_timer += delta_time

        if self.color == (255, 0, 0):
            # Если ты пришлешь документацию по частицам, переделаем это на ParticleSystem
            self.flash_timer -= delta_time  # Нужно создать flash_timer = 1.0 в __init__
            if self.flash_timer <= 0:
                self.color = (255, 255, 255)
                self.flash_timer = 1.0

    def shoot(self):
        if self.overheated:
            return False
        self.heat += 20
        if self.heat >= 100:
            self.heat = 100
            self.overheated = True
        return True

    def reset_heat(self):
        self.heat = 0
        self.overheated = False
