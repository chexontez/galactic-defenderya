import arcade
import random
from src.constants import *


class Enemy(arcade.Sprite):
    def __init__(self):
        # Используем спрайт enemy.png
        super().__init__(str(IMAGES_DIR / "enemy.png"), scale=1.0)

        self.center_x = random.randint(30, SCREEN_WIDTH - 30)
        self.center_y = SCREEN_HEIGHT + 40
        self.change_y = -ENEMY_SPEED
        self.hp = 1
        self.shoot_timer = random.uniform(1.0, 3.0)

    def update(self, delta_time: float = 1 / 60):
        # Движение вниз
        self.center_y += self.change_y
        super().update(delta_time)
        self.shoot_timer -= delta_time
        # Удаление, если улетел за экран
        if self.top < 0:
            self.kill()

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            return True
        return False

    # Метод стрельбы
    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = random.uniform(1.5, 4.0)  # Сброс таймера
            return True
        return False
