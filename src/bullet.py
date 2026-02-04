import arcade
from src.constants import *


class Bullet(arcade.Sprite):
    # В __init__
    def __init__(self, x, y, is_super=False, is_enemy=False):
        super().__init__(str(IMAGES_DIR / "bullet.png"), scale=0.8 if not is_super else 1.5)
        self.center_x = x
        self.center_y = y
        self.is_super = is_super
        self.is_enemy = is_enemy

        # Если враг — летит вниз, если игрок — вверх
        direction = -1 if is_enemy else 1
        self.change_y = BULLET_SPEED * direction * (1.5 if is_super else 1.0)
        self.damage = 3 if is_super else 1

        # Красный фильтр для вражеских пуль
        if is_enemy:
            self.color = (255, 100, 100)  # Красный оттенок

    def update(self, delta_time: float = 1 / 60):
        # Движение вверх
        self.center_y += self.change_y

        # Удаление, если улетела за экран
        if self.bottom > SCREEN_HEIGHT:
            self.kill()
