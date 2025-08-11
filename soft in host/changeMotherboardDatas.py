import ctypes
import sys
import os
from pywinauto.findwindows import ElementNotFoundError
import time
import pyautogui
from pywinauto import Application
import random

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


def launch_phoenix(phoenix_path):
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", phoenix_path, None, None, 1
        )
        print(f"Запускаем Phoenix из {phoenix_path}...")
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Ошибка при запуске Phoenix: {e}")
        return False


def find_and_click_settings(app):
    try:
        # Получаем главное окно
        main_window = app.window(title="Phoenix BIOS Editor Pro")
        main_window.set_focus()
        time.sleep(0.3)
        rect = main_window.rectangle()
        print(f"Окно найдено: {main_window.window_text()}")

        #Открываем файл .ROM
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(1)
        pyautogui.hotkey('alt', 'd')
        time.sleep(1)
        pyautogui.write(r"C:\Users\neon4\Desktop\Motherboards\Asus\6006.ROM")
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(5)

        #Закрываем два первых окна
        pyautogui.hotkey('ctrl','f4')
        pyautogui.hotkey('ctrl','f4')

        #Генерируем рандомные 12значные числа
        serial_number = []
        for _ in range(12):
            i = random.randint(0, 9)
            serial_number.append(str(i))

        all_datas = ''.join(serial_number)

        new_number = []
        for _ in range(12):
            i = random.randint(0, 9)
            new_number.append(str(i))

        new = ''.join(new_number)

        action_sequence = [
            # Пишем Serial Number
            {'clicks': [(1046, 258), (1046, 258)],
             'text': f"'{all_datas}'", 'delay': 1},
            {'enter': True},
            {'clicks': [(1068, 378), (1068, 378)],
             'text': f"'{all_datas}'", 'delay': 1},
            {'enter': True},
            {'clicks': [(1039, 326), (1039, 326)],
             'text': f"'{new}'", 'delay': 1},
            {'enter': True}
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

            if action.get('enter'):
                pyautogui.press('enter')

        pyautogui.hotkey('ctrl', 'u')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')

        number_file = int(input("Введите номер файла (Только цифры): "))
        time.sleep(4)
        pyautogui.write(f"6006_{number_file}.ROM")
        time.sleep(2)
        pyautogui.press('enter')

        return True

    except Exception as e:
        print(f"Ошибка выполнения: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("Скрипт запущен с правами администратора!")
    print("=" * 50 + "\n")

    phoenix_path = r"C:\Users\neon4\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Phoenix BIOS Editor\Phoenix BIOS Editor.lnk"

    try:
        app = Application(backend="uia").connect(title="Phoenix BIOS Editor Pro")
        print("Успешное подключение к запущенному Phoenix!")
    except ElementNotFoundError:
        print("Phoenix не запущен. Пытаемся запустить...")
        if launch_phoenix(phoenix_path):
            time.sleep(7)
            try:
                app = Application(backend="uia").connect(title="Phoenix BIOS Editor Pro")
                print("Успешное подключение после запуска!")
            except Exception as e:
                print(f"Не удалось подключиться к Phoenix: {e}")
                return
        else:
            return

    if not find_and_click_settings(app):
        print("Не удалось взаимодействовать с Settings")

    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    run_as_admin()
    main()