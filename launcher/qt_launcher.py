import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic


class GameLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "startwindow.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("Galactic Defender - Настройки")
        self.sumbit.clicked.connect(self.launch_game)

    def launch_game(self):
        # Исправлено: берем текст из правильных полей 'width' и 'height'
        try:
            w = int(self.width.text())
            h = int(self.height.text())
        except:
            w, h = 800, 600

        config_data = {
            "screen_width": w,
            "screen_height": h,
            "player_speed": self.player_speed.value(),
            "enemy_speed": self.enemy_speed.value(),
            "laser_speed": self.laser_speed.value(),
            "player_hp": 5
        }

        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "current_config.json")

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)

        project_root = os.path.dirname(os.path.dirname(__file__))
        # Запускаем через main.py в корне
        main_script = os.path.join(project_root, "main.py")
        subprocess.Popen([sys.executable, main_script], cwd=project_root)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameLauncher()
    window.show()
    sys.exit(app.exec())
