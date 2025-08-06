import ctypes
import sys
import os
from pywinauto.findwindows import ElementNotFoundError
import time
import pyautogui
from pywinauto import Application

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit(0)


def launch_ragdoll(ragdoll_path):
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", ragdoll_path, None, None, 1
        )
        print(f"Запускаем Ragdoll из {ragdoll_path}...")
        return True
    except Exception as e:
        print(f"Ошибка при запуске Ragdoll: {e}")
        return False

def find_and_click_settings(app):
    main_window = app.window(title="Ragdoll")
    main_window.set_focus()
    time.sleep(0.3)  # Важно для некоторых приложений
    rect = main_window.rectangle()
    print("Окно найдено:", main_window.window_text())

    try:
        click_sequence = [
            (rect.left + 53, rect.top + 27),  # Первая точка
            (rect.left + 43, rect.top + 283),  # Вторая точка
            (rect.left + 103, rect.top + 24)  # Третья точка
        ]
        for x, y in click_sequence:
            pyautogui.click(x, y)
            time.sleep(0.2)  #
        pyautogui.write("Hello Ragdoll!", interval=0.05)  # Медленный ввод
        time.sleep(1)

        return True
    except Exception as e:
        print(f"Ошибка при клике по координатам: {e}")
        return False

def main():
    print("=" * 50)
    print("Скрипт запущен с правами администратора!")
    print("=" * 50 + "\n")

    ragdoll_path = r"C:\Users\neon4\Desktop\Launcher.exe" # Замените на реальный путь

    try:
        app = Application(backend="uia").connect(title="Ragdoll")
        print("Успешное подключение к запущенному Ragdoll!")
    except ElementNotFoundError:
        print("Ragdoll не запущен. Пытаемся запустить...")
        if launch_ragdoll(ragdoll_path):
            time.sleep(7)
            try:
                app = Application(backend="uia").connect(title="Ragdoll")
                print("Успешное подключение после запуска!")
            except Exception as e:
                print(f"Не удалось подключиться к Ragdoll: {e}")
                return
        else:
            return

    if not find_and_click_settings(app):
        print("Не удалось взаимодействовать с Settings")

    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    run_as_admin()
    main()