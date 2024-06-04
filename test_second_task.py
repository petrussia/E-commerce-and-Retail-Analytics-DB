'''
скрипт демонстрирует проверку и работостособность моего 2 запроса
P.S. для верности работы на вашем устройстве, смените в строке 11 данные на свои
'''

import pandas as pd
from sqlalchemy import create_engine
from fix_json import fix_incorrect_json

# Для начала я настрою строку подключения к моей СУБД PostgreSQL
try:
    DATABASE_URI = 'postgresql://user:1@localhost:5432/Retails'
except:
    # в случае сбоя подключения будет выведено сообщение  в STDOUT
    print('Can`t establish connection to database')
    exit(2)
# Создаём движок engine для подключения к БД
engine = create_engine(DATABASE_URI)

#удаляем ошибки в файле orders из json
file_path = 'orders.csv'
fix_incorrect_json(file_path)
# print(orders_df.head())
# Читаем данные из CSV-файлов
orders_df = pd.read_csv('correct_orders.csv', encoding='utf8')
product_df = pd.read_csv('product.csv', encoding='utf8')
store_df = pd.read_csv('store.csv', encoding='utf8')
sales_df = pd.read_csv('sales.csv', encoding='utf8')
user_df = pd.read_csv('user.csv', encoding='utf8')

# Загружаем данные из DataFrame в соответствующие таблицы в базе данных
orders_df.to_sql('orders', engine, if_exists='replace', index=False)
product_df.to_sql('product', engine, if_exists='replace', index=False)
store_df.to_sql('store', engine, if_exists='replace', index=False)
sales_df.to_sql('sales', engine, if_exists='replace', index=False)
user_df.to_sql('user', engine, if_exists='replace', index=False)

# Читаем SQL-кода из файла
with open('result_task_2.txt', 'r', encoding='utf-8') as file:
    sql_code = file.read()

# Выделяем вход в context manager для подключения
with engine.connect() as connection:
    # Выполняем SQL-запроса и получение результата в виде DataFrame
    result_df = pd.read_sql(sql_code, connection)

# Вывод результата в консоль
print(result_df)
