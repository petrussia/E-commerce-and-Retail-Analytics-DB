# обработка csv таблиц и автоматическое исправление в них ошибок
import csv


def fix_incorrect_json(file_path):
    """
    Функция заменяет каждую одинарную кавычку в файле на двойную.
    True и False с верхнего регистра на нижний
    """
    try:
        # Открываем файл для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Заменяем каждую одинарную кавычку на двойную
        modified_content = content.replace('"', '').replace("'", '"').replace(": False", ": false").replace(": True",
                                                                                                            ": true").split(
            '\n')
        # Открываем файл для записи и записываем модифицированное содержимое
        with open('correct_orders.csv', 'w', newline='', encoding='utf-8') as file:
            # Объект для записи в CSV
            writer = csv.writer(file, delimiter=',')
            flag = 0
            # Обработка каждой строки
            for row in modified_content:
                if flag == 0:
                    rows = row.split(',')
                if flag == 0:
                    rows = row.split(',', 4)
                writer.writerow(rows)
        file.close()
        # print(f"Заменены все одинарные кавычки на двойные в файле: {file}")
    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")

# file_path = 'orders.csv'
# fix_incorrect_json(file_path)
#
# df = pd.read_csv('correct_orders.csv', engine='python', encoding='utf-8')
# print(f"Заголовки: {list(df.columns)}")
# print("Первые 5 строк данных:")
# print(df.head())
