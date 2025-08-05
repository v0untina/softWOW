import pandas as pd
def findemail():
    try:
        df = pd.read_excel('file.xlsx', sheet_name='Sheet1', header=None)

        # Перебираем строки
        for index, row in df.iterrows():
            email = row[0]
            text = row[1]
            neweail = list(email)
            print(neweail)
            if pd.isna(text) or str(text).strip() == '':
                if "@" in email:
                    print(f"Найдена пустая ячейка в строке {index + 1}: {email}")
                    return email
        else:
            print("Пустых ячеек не найдено")

    except FileNotFoundError:
        print("Ошибка: файл не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")