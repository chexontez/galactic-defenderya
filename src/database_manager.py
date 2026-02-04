import sqlite3
from datetime import datetime
from src.constants import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                played_at TEXT,
                game_duration REAL,
                enemies_killed INTEGER,
                super_shots_fired INTEGER
            )
        """)
        conn.commit()

def save_game_result(duration, kills, super_shots):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO game_logs (played_at, game_duration, enemies_killed, super_shots_fired)
            VALUES (?, ?, ?, ?)
        """, (now, duration, kills, super_shots))
        conn.commit()

def get_all_logs():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Берем последние 10 игр для отображения
        cursor.execute("SELECT played_at, game_duration, enemies_killed, super_shots_fired FROM game_logs ORDER BY id DESC LIMIT 10")
        return cursor.fetchall()