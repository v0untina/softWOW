import ctypes
import os
import sys
import time
import win32api
import win32con
from datetime import datetime
from pywinauto import Application


class ClickRecorder:
    def __init__(self):
        self.coordinates = []
        self.output_file = "mouse_coordinates.txt"
        self.running = True

    def record_clicks(self):
        """Записывает координаты всех кликов до нажатия правой кнопки"""
        print("Инструкция:")
        print("1. ЛКМ - записать координаты клика")
        print("2. ПКМ - завершить запись")
        print("3. ESC - экстренный выход")
        print("\nНачинаем запись координат...\n")

        with open(self.output_file, "a") as f:
            f.write(f"\n\nСессия записи: {datetime.now()}\n")
            f.write("Формат: [Время] Абсолютные (X, Y) | Относительные (X, Y)\n")

        while self.running:
            # Проверка на выход по ESC
            if win32api.GetAsyncKeyState(win32con.VK_ESCAPE) < 0:
                print("\nЭкстренное завершение по ESC")
                self.running = False
                break

            # Проверка ЛКМ
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
                abs_x, abs_y = win32api.GetCursorPos()
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                # Пытаемся получить относительные координаты
                try:
                    app = Application(backend="uia").connect(title="Ragdoll")
                    window = app.window(title="Ragdoll")
                    rect = window.rectangle()
                    rel_x = abs_x - rect.left
                    rel_y = abs_y - rect.top
                    rel_info = f"Относительные: ({rel_x}, {rel_y})"
                except:
                    rel_info = "Относительные: не определены"

                # Записываем в консоль
                print(f"[{timestamp}] Абсолютные: ({abs_x}, {abs_y}) | {rel_info}")

                # Записываем в файл
                with open(self.output_file, "a") as f:
                    f.write(f"[{timestamp}] ({abs_x}, {abs_y}) | ({rel_x}, {rel_y})\n")

                self.coordinates.append((abs_x, abs_y, rel_x, rel_y))
                time.sleep(0.3)  # Задержка для предотвращения дублирования

            # Проверка ПКМ для завершения
            if win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0:
                print("\nЗавершение записи по ПКМ")
                self.running = False
                break

            time.sleep(0.01)


def main():
    # Проверка прав администратора
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Перезапуск с правами администратора...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
    except:
        pass

    print("=" * 50)
    print("Многоточечный регистратор координат мыши")
    print("=" * 50)

    recorder = ClickRecorder()
    recorder.record_clicks()

    # Вывод статистики
    print("\nСтатистика:")
    print(f"Всего записано кликов: {len(recorder.coordinates)}")
    if recorder.coordinates:
        print("Последние 5 координат:")
        for coord in recorder.coordinates[-5:]:
            print(f"- Абсолютные: ({coord[0]}, {coord[1]}) | Относительные: ({coord[2]}, {coord[3]})")

    print(f"\nВсе координаты сохранены в файл: {recorder.output_file}")
    input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()