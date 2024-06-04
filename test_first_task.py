'''
скрипт демонстрирует проверку и работостособность моего 1  запроса
P.S. для верности работы на вашем устройстве, смените в строке 11 данные на свои
'''

import pandas as pd
from sqlalchemy import create_engine

# Для начала я настрою строку подключения к моей СУБД PostgreSQL
try:
    DATABASE_URI = 'postgresql://user:1@localhost:5432/Retails'
except:
    # в случае сбоя подключения будет выведено сообщение  в STDOUT
    print('Can`t establish connection to database')
    exit(2)
# Создаём движок engine для подключения к БД
engine = create_engine(DATABASE_URI)

# Читаем данные из CSV-файлов
events_df = pd.read_csv('events.csv', encoding='utf8')

# Загружаем данные из DataFrame в соответствующие таблицы в базе данных
events_df.to_sql('events', engine, if_exists='replace', index=False)

# Читаем SQL-кода из файла
with open('result_task_1.txt', 'r', encoding='utf-8') as file:
    sql_code = file.read()

# Выделяем вход в context manager для подключения
with engine.connect() as connection:
    # Выполняем SQL-запроса и получение результата в виде DataFrame
    result_df = pd.read_sql(sql_code, connection)

# Вывод результата в консоль
print(result_df)
