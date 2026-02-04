import arcade
import random
from src.constants import *
from src.database_manager import save_game_result, get_all_logs, init_db
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy


# (Если нужен астероид, создай аналогичный файл src/asteroid.py, пока заглушка в коде)

class GalacticDefender(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        init_db()

        # Текстовые объекты (оптимизация)
        self.ui_text_hp = arcade.Text("", 20, 45, arcade.color.WHITE, 14, bold=True)
        self.ui_text_score = arcade.Text("", 120, 45, arcade.color.WHITE, 14, bold=True)
        self.ui_text_time = arcade.Text("", 250, 45, arcade.color.WHITE, 14, bold=True)

        # Размеры кнопок меню для кликов
        self.btn_play_rect = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50)  # x, y, w, h
        self.btn_logs_rect = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70, 200, 50)
        self.btn_exit_rect = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140, 200, 50)

        self.load_sounds()
        self.setup()

    def load_sounds(self):
        try:
            self.snd_shoot = arcade.load_sound(SOUNDS_DIR / "shoot.wav")
            self.snd_hit_ship = arcade.load_sound(SOUNDS_DIR / "hitship.wav")
            self.snd_hit_enemy = arcade.load_sound(SOUNDS_DIR / "hitenemy.wav")
            self.snd_super = arcade.load_sound(SOUNDS_DIR / "supershoot.wav")
            self.snd_end = arcade.load_sound(SOUNDS_DIR / "end.wav")
            self.snd_music = arcade.load_sound(SOUNDS_DIR / "music.wav")

            if self.snd_music:
                arcade.play_sound(self.snd_music, volume=0.2, loop=True)
        except Exception:
            self.snd_shoot = self.snd_hit_ship = self.snd_hit_enemy = \
                self.snd_super = self.snd_end = self.snd_music = None

    def setup(self):
        self.game_state = "MENU"
        self.score = 0
        self.game_time = 0.0
        self.super_shots_fired = 0
        self.enemy_timer = 0
        self.logs_data = get_all_logs()

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()

        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        self.stars = []
        for _ in range(70):
            self.stars.append(
                [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.random() * 2 + 1])

    def on_draw(self):
        self.clear()

        # Фон
        for s in self.stars:
            arcade.draw_circle_filled(s[0], s[1], s[2], arcade.color.WHITE)

        if self.game_state in ("PLAYING", "PAUSED", "GAME_OVER"):
            self.player_list.draw()
            self.enemy_list.draw()
            self.bullet_list.draw()
            self.asteroid_list.draw()
            self.draw_ui()

        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "STATS":
            self.draw_stats_screen()
        elif self.game_state == "PAUSED":
            self.draw_pause_overlay()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()

    def draw_ui(self):
        # Панель (Left, Right, Bottom, Top)
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, UI_HEIGHT, COLOR_HUD)
        arcade.draw_line(0, UI_HEIGHT, SCREEN_WIDTH, UI_HEIGHT, arcade.color.GRAY, 2)

        # Текст
        self.ui_text_hp.text = f"HP: {self.player_sprite.hp}"
        self.ui_text_hp.draw()

        self.ui_text_score.text = f"СЧЕТ: {self.score}"
        self.ui_text_score.draw()

        self.ui_text_time.text = f"ВРЕМЯ: {int(self.game_time)}"
        self.ui_text_time.draw()

        # --- Шкала Нагрева (HEAT) ---
        arcade.draw_text("HEAT", 400, 55, arcade.color.WHITE, 10, anchor_x="center")
        # Рамка
        arcade.draw_lrbt_rectangle_outline(350, 450, 30, 45, arcade.color.WHITE, 1)
        # Заливка
        heat_pct = min(self.player_sprite.heat / MAX_HEAT, 1.0)
        if heat_pct > 0:
            fill_w = 100 * heat_pct
            c = arcade.color.RED if self.player_sprite.overheated else COLOR_HEAT_BAR
            arcade.draw_lrbt_rectangle_filled(351, 351 + fill_w - 2, 31, 44, c)

        # --- Шкала Супер-выстрела (SUPER) ---
        arcade.draw_text("SUPER", 550, 55, arcade.color.WHITE, 10, anchor_x="center")
        arcade.draw_lrbt_rectangle_outline(500, 600, 30, 45, arcade.color.WHITE, 1)
        super_pct = min(self.player_sprite.super_shot_timer / SUPER_SHOT_COOLDOWN, 1.0)
        if super_pct > 0:
            fill_w = 100 * super_pct
            arcade.draw_lrbt_rectangle_filled(501, 501 + fill_w - 2, 31, 44, COLOR_SUPER_BAR)

    def draw_menu(self):
        arcade.draw_text("GALACTIC DEFENDER", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                         arcade.color.CYAN, 40, anchor_x="center", bold=True)

        self._draw_btn(self.btn_play_rect, "ИГРАТЬ")
        self._draw_btn(self.btn_logs_rect, "ИСТОРИЯ")
        self._draw_btn(self.btn_exit_rect, "ВЫХОД")

    def _draw_btn(self, rect, text):
        x, y, w, h = rect
        l, r, b, t = x - w / 2, x + w / 2, y - h / 2, y + h / 2
        arcade.draw_lrbt_rectangle_outline(l, r, b, t, arcade.color.WHITE, 2)
        arcade.draw_text(text, x, y, arcade.color.WHITE, 14, anchor_x="center", anchor_y="center")

    def draw_stats_screen(self):
        arcade.draw_text("ИСТОРИЯ ИГР", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80, arcade.color.WHITE, 30, anchor_x="center")

        y = SCREEN_HEIGHT - 150
        if not self.logs_data:
            arcade.draw_text("Пусто...", SCREEN_WIDTH / 2, y, arcade.color.GRAY, 14, anchor_x="center")

        for i, log in enumerate(self.logs_data[:5]):
            # log: id, played_at, duration, kills, super_shots
            row = f"{log[0]} | {int(log[1])} сек | Убито: {log[2]}"
            arcade.draw_text(row, SCREEN_WIDTH / 2, y - (i * 30), arcade.color.YELLOW, 12, anchor_x="center")

        arcade.draw_text("ESC - Назад", SCREEN_WIDTH / 2, 50, arcade.color.GRAY, 10, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state == "MENU":
            if self._is_click(x, y, self.btn_play_rect):
                self.game_state = "PLAYING"
                self.score = 0  # Сброс счета при рестарте
            elif self._is_click(x, y, self.btn_logs_rect):
                self.logs_data = get_all_logs()
                self.game_state = "STATS"
            elif self._is_click(x, y, self.btn_exit_rect):
                self.close()

    def _is_click(self, x, y, rect):
        bx, by, bw, bh = rect
        return (bx - bw / 2 < x < bx + bw / 2) and (by - bh / 2 < y < by + bh / 2)

    def on_update(self, delta_time):
        if self.game_state == "PLAYING":
            self.game_time += delta_time
            self.enemy_timer += delta_time

            # Обновление спрайтов (Player требует delta_time)
            self.player_list.update(delta_time)
            self.enemy_list.update()
            self.bullet_list.update()

            # Спавн врагов
            if self.enemy_timer > ENEMY_SPAWN_RATE:
                self.enemy_list.append(Enemy())
                self.enemy_timer = 0

            # Коллизии: Пули -> Враги
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if hit_list:
                    bullet.kill()
                    for enemy in hit_list:
                        if enemy.take_damage(bullet.damage):  # Если умер
                            self.score += 10
                            if self.snd_hit_enemy: arcade.play_sound(self.snd_hit_enemy)

            # Коллизии: Враги -> Игрок
            hit_player = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
            for enemy in hit_player:
                enemy.kill()
                self.player_sprite.hp -= 1
                if self.snd_hit_ship: arcade.play_sound(self.snd_hit_ship)
                if self.player_sprite.hp <= 0:
                    self.game_over()

            # Анимация звезд
            for s in self.stars:
                s[1] -= s[2]
                if s[1] < 0: s[1] = SCREEN_HEIGHT

            # стрельба
            for enemy in self.enemy_list:
                if enemy.shoot():
                    bullet = Bullet(enemy.center_x, enemy.bottom, is_enemy=True)
                    self.bullet_list.append(bullet)

            asteroids_hit = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
            for asteroid in asteroids_hit:
                self.player_sprite.hp -= 2
                asteroid.kill()
                # Эффект красного мигания
                self.player_sprite.color = (255, 0, 0)
                # Нужно добавить таймер в Player, чтобы через 1 сек вернуть цвет (255,255,255)

    def on_key_press(self, key, modifiers):
        if self.game_state == "PLAYING":
            if key == arcade.key.ESCAPE:
                self.game_state = "PAUSED"
            elif key in (arcade.key.LEFT, arcade.key.A):
                self.player_sprite.change_x = -self.player_sprite.speed
            elif key in (arcade.key.RIGHT, arcade.key.D):
                self.player_sprite.change_x = self.player_sprite.speed
            elif key == arcade.key.SPACE:
                if self.player_sprite.shoot():
                    self.bullet_list.append(Bullet(self.player_sprite.center_x, self.player_sprite.top))
                    if self.snd_shoot: arcade.play_sound(self.snd_shoot)
            elif key == arcade.key.X:
                if self.player_sprite.super_shot_timer >= SUPER_SHOT_COOLDOWN:
                    # Супер выстрел (3 пули)
                    self.bullet_list.append(Bullet(self.player_sprite.center_x, self.player_sprite.top, is_super=True))
                    self.bullet_list.append(
                        Bullet(self.player_sprite.center_x - 20, self.player_sprite.top - 10, is_super=True))
                    self.bullet_list.append(
                        Bullet(self.player_sprite.center_x + 20, self.player_sprite.top - 10, is_super=True))

                    if self.snd_super: arcade.play_sound(self.snd_super)
                    self.player_sprite.super_shot_timer = 0
                    self.player_sprite.reset_heat()
                    self.super_shots_fired += 1

        elif self.game_state == "STATS" and key == arcade.key.ESCAPE:
            self.game_state = "MENU"
        elif self.game_state == "PAUSED" and key == arcade.key.ESCAPE:
            self.game_state = "PLAYING"
        elif self.game_state == "GAME_OVER":
            if key == arcade.key.ENTER:
                self.setup()
            elif key == arcade.key.ESCAPE:
                self.game_state = "MENU"

    def on_key_release(self, key, modifiers):
        if self.game_state == "PLAYING":
            if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
                self.player_sprite.change_x = 0

    def draw_pause_overlay(self):
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, UI_HEIGHT, SCREEN_HEIGHT, (0, 0, 0, 150))
        arcade.draw_text("ПАУЗА", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, 40, anchor_x="center")

    def draw_game_over_screen(self):
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, UI_HEIGHT, SCREEN_HEIGHT, (100, 0, 0, 200))
        arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, arcade.color.RED, 50, anchor_x="center",
                         bold=True)
        arcade.draw_text(f"SCORE: {self.score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20, arcade.color.WHITE, 20,
                         anchor_x="center")
        arcade.draw_text("ENTER - Retry", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60, arcade.color.GRAY, 14,
                         anchor_x="center")

    def game_over(self):
        if self.snd_end: arcade.play_sound(self.snd_end)
        self.game_state = "GAME_OVER"
        save_game_result(self.game_time, self.score, self.super_shots_fired)


if __name__ == "__main__":
    window = GalacticDefender()
    arcade.run()
