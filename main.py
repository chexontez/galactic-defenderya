import sys
import os
import subprocess

def main():
    launcher_path = os.path.join(os.path.dirname(__file__), "launcher", "qt_launcher.py")
    subprocess.run([sys.executable, launcher_path])

if __name__ == "__main__":
    main()