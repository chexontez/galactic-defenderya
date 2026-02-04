import sys
import os
import subprocess

def main():
    launcher_path = os.path.join(os.path.dirname(__file__), "launcher", "qt_launcher.py")

    if not os.path.exists(launcher_path):
        print(f"Ошибка: Не найден файл лаунчера по пути {launcher_path}")
        return

    try:
        subprocess.run([sys.executable, launcher_path])
    except Exception as e:
        print(f"Не удалось запустить лаунчер: {e}")

if __name__ == "__main__":
    main()