import arcade
import random
from src.constants import *


class Asteroid(arcade.Sprite):
    def __init__(self):
        # Используем спрайт meteorit.png
        super().__init__(str(IMAGES_DIR / "meteorit.png"), scale=random.uniform(0.5, 1.2))

        self.center_x = random.randint(50, SCREEN_WIDTH - 50)
        self.center_y = SCREEN_HEIGHT + 50
        self.change_y = -random.uniform(1.0, 3.0)
        self.hp = 2
        self.color = (255, 255, 255)

    def update(self, delta_time: float = 1 / 60):
        self.center_y += self.change_y

        if self.top < 0:
            self.kill()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            return True
        return False