import json
from pathlib import Path

SRC_DIR = Path(__file__).parent
PROJECT_ROOT = SRC_DIR.parent

ASSETS_DIR = SRC_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

CONFIG_PATH = PROJECT_ROOT / "config" / "current_config.json"
DB_PATH = PROJECT_ROOT / "database" / "logs.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_config():
    default_settings = {
        "screen_width": 800,
        "screen_height": 600,
        "player_speed": 5,
        "enemy_speed": 3,
        "laser_speed": 8,
        "player_hp": 5
    }

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**default_settings, **config}
        except Exception as e:
            print(f"ошибка чтения конфига: {e}")
    else:
        pass

    return default_settings


CONFIG = load_config()

SCREEN_WIDTH = int(CONFIG["screen_width"])
SCREEN_HEIGHT = int(CONFIG["screen_height"])
SCREEN_TITLE = "Galactic Defender"

PLAYER_SPEED = float(CONFIG["player_speed"])
ENEMY_SPEED = float(CONFIG["enemy_speed"])
BULLET_SPEED = float(CONFIG["laser_speed"])
PLAYER_HP = int(CONFIG["player_hp"])

UI_HEIGHT = 80
GAME_ZONE_BOTTOM = UI_HEIGHT

ENEMY_SPAWN_RATE = 1.5
ASTEROID_SPAWN_RATE = 2.0
SUPER_SHOT_COOLDOWN = 10.0
MAX_HEAT = 100
HEAT_PER_SHOT = 15
COOLING_RATE = 25

COLOR_HUD = (30, 30, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_HEAT_BAR = (255, 69, 0)
COLOR_SUPER_BAR = (0, 191, 255)