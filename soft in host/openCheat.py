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
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Ошибка при запуске Ragdoll: {e}")
        return False


def find_and_click_settings(app):
    try:
        # Получаем главное окно
        main_window = app.window(title="Ragdoll")
        main_window.set_focus()
        time.sleep(0.3)
        rect = main_window.rectangle()
        print(f"Окно найдено: {main_window.window_text()} (Позиция: {rect.left}, {rect.top})")

        action_sequence = [
            # Заход в Settings|Add и Profile Name
            {'clicks': [(53, 27), (43, 283),(103,24)],
             'text': "Profile Name", 'delay': 1},

            # Username
            {'clicks': [(94, 73)],
             'text': "Username", 'delay': 1},

            # Password
            {'clicks': [(208, 75)],
             'text': "Password", 'delay': 1},

            #Realm
            {'clicks': [(187, 126)],
             'text': "Realm", 'delay': 1},

            #Character
            {'clicks': [(148, 166)],
             'text': "Character", 'delay': 1},

            #Apply
            {'clicks': [(322, 495)],'delay': 5},

            #Settings|License
            {'clicks': [(208, 26),(162,109)],
              'delay': 5},

            {'text':"GKRMEGKEGMERKKLlgmelmg00000", 'delay': 5},
            #Apply
            {'clicks': [(370, 108)], 'delay': 5},

            #Scroll
            {'clicks': [(425,405),(425,405)], 'delay': 5},

        ]

        for action in action_sequence:
            for _ in range(action.get('repeat', 1)):
                for rel_x, rel_y in action.get('clicks', []):
                    abs_x = rect.left + rel_x
                    abs_y = rect.top + rel_y
                    pyautogui.click(abs_x, abs_y)
                    time.sleep(0.2)

            if 'text' in action:
                pyautogui.write(action['text'], interval=0.1)
                time.sleep(action['delay'])

        return True

    except Exception as e:
        print(f"Ошибка выполнения: {str(e)}")
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