import time
import random
from parserfio import getfio
from findemail import findemail
from playwright.sync_api import sync_playwright
import keyboard
from randomchars import generate_random_chars
import pyperclip

def human_delay(min=0.5, max=1.5):
    time.sleep(random.uniform(min, max))


with sync_playwright() as p:
    # 1. Настройка браузера (добавляем реалистичные параметры)
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized"
        ]
    )

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        locale="ru-RU"
    )
    page = context.new_page()

    # 2. Надежная загрузка страницы
    try:
        page.goto(
            "https://account.battle.net/creation?locale=ru-ru",
            wait_until="domcontentloaded",
        )
        human_delay(1, 2)  # Дополнительная пауза
    except:
        print("Перезагрузка страницы...")
        page.reload()


    # 3. Улучшенное ожидание элементов
    def safe_wait(selector, action="click", timeout=150000):
        for _ in range(3):  # 3 попытки
            try:
                elem = page.locator(selector)
                elem.wait_for(state="visible", timeout=timeout)
                human_delay(0.3, 0.7)
                if action == "click":
                    elem.click()
                elif action == "type":
                    return elem
                return True
            except:
                print(f"Повторная попытка для {selector}")
        return False


    # 4. Заполнение формы с перехватом ошибок
    try:
        # Выбор страны
        if safe_wait("#capture-country"):
            page.select_option("#capture-country", value="UKR")
            human_delay(1,2)

        # Ввод даты
        if safe_wait("#dob-field-inactive", "click"):
            human_delay(1,2)
            days=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"]
            months=["01","02","03","04","05","06","07","08","09","10","11","12"]
            day = random.choice(days)
            month = random.choice(months)
            year = random.choice(range(1970,2006))
            date_parts = [str(day), str(month), str(year)]
            print("Введенная дата:",date_parts)
            for i, part in enumerate(date_parts):
                for char in part:
                    page.keyboard.type(char)
                    human_delay(0.1, 0.2)
                if i < 2:
                    page.keyboard.press("Tab")
                    human_delay(0.3, 0.5)

        # Кнопка продолжения
        if safe_wait(".step__button--primary", "click"):
            print("Регион и дата рождения введены!")

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")

    human_delay(1, 2)

    #5 Ввод данных ФИО из парсера
    try:
        surname,name = getfio()
        if safe_wait("#capture-first-name", "click"):
            for i in range(len(name)):
                page.keyboard.type(name[i])
                human_delay(0.5, 1.0)

        human_delay(1, 2)

        if safe_wait("#capture-last-name", "click"):
            for i in range(len(surname)):
                page.keyboard.type(surname[i])
                human_delay(0.5, 1.0)

        print("Введены Имя и Фамилия", name,surname)

    except Exception as e:
        print("Пиздец ошибка!!!",e)

    human_delay(1, 2)

    if safe_wait(".step__button--primary", "click"):
        print("Имя и фамилия введены!")

    #6 Вводим почту из таблицы
    try:
        email = list(findemail())
        human_delay(1, 2)
        if safe_wait("#capture-email", "click"):
            for i in range(len(email)):
                page.keyboard.type(email[i])
                human_delay(0.5, 1.0)

        if safe_wait(".step__button--primary", "click"):
            print("Имя и фамилия введены!")
        print("Введен email", email)
        human_delay(1, 2)


    except Exception as e:
        print("Пиздец ошибка!!!",e)

        human_delay(1, 2)


    #7 Ставим галочки
    try:
        # Клик напрямую через JavaScript, минуя перехват событий
        page.evaluate('''() => {
            document.getElementById('capture-opt-in-blizzard-news-special-offers').click();
        }''')
        human_delay(1, 2)
        page.evaluate('''() => {
            const checkbox = document.querySelector('input.step__checkbox[name="tou-agreements-implicit"][type="checkbox"]');
            if (checkbox) {
                checkbox.click();
                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            }
            return false;
        }''')
        human_delay(1, 2)
        # Кнопка подтверждения
        if safe_wait("#flow-form-submit-btn", "click"):  # Селектор для основной кнопки принятия
            print("Соглашения подписаны!")
    except Exception as e:
        print("Ошибка при принятии соглашений:", e)

        human_delay(1, 4)
    #8 Пароль
    try:
        password = ''.join(email[:-1])
        if safe_wait("#capture-password", "click"):
            for i in range(len(password)):
                page.keyboard.type(password[i])
                human_delay(0.5, 1.0)

        if safe_wait("#flow-form-submit-btn", "click"):  # Селектор для основной кнопки принятия
            print("Пароль",password,"сохранен!")
    except Exception as e:
        print(e)
        d

    #9 Юзернейм
    try:
        if safe_wait("#suggest-battletag-btn", "click"):
            print("Ник изменен рандомно")
        if safe_wait("#capture-battletag", "click"):
            time.sleep(1)
            for _ in range(16):
                keyboard.press_and_release('backspace')
                time.sleep(0.1)

            new_chars = generate_random_chars(random.randint(5, 10))
            keyboard.write(new_chars)
            time.sleep(0.5)

            # 4. Копируем новый ник
            keyboard.press_and_release('ctrl+a')
            time.sleep(0.3)
            keyboard.press_and_release('ctrl+c')
            time.sleep(0.3)
            new_nick = pyperclip.paste().strip()

        human_delay(1,4)

        if safe_wait("#flow-form-submit-btn", "click"):
            print("Новый ник:",new_nick)
            print("Регистрация завершена,Все данные добавлены в таблицу")

    except Exception as e:
        print(e)
    human_delay(100,200)

    try:
        print("")
    except Exception as e:
        print(e)