# основной скрипт для задания 3.2
import pandas as pd
import json
from sklearn.linear_model import LinearRegression # будем использовать модель с машинным обучением scikit-learn
                                                  # для прогнозирования покупок с помощью модели линейной регрессии
import numpy as np

pd.set_option('mode.chained_assignment', None)
# Загрузим данные из CSV наших табличек в пандас
orders = pd.read_csv('correct_orders.csv')
sales = pd.read_csv('sales.csv')
store = pd.read_csv('store.csv')
product = pd.read_csv('product.csv')

# Сначала отфильтруем только выкупленные заказы
sales_filtered = sales[(sales['is_accepted'] == True) & (sales['is_canceled'] == False)]

# Группируем и фильтруем заказы на основе отфильтрованных продаж
valid_order_ids = sales_filtered['order_id'].unique()
orders_filtered = orders[orders['order_id'].isin(valid_order_ids)]

# # Преобразуем JSON-объекты product_info в столбцы
orders_filtered['product_info'] = orders_filtered['product_info'].apply(json.loads)
orders_exploded = orders_filtered.explode('product_info')
orders_exploded = pd.concat(
    [orders_exploded.drop(['product_info'], axis=1), orders_exploded['product_info'].apply(pd.Series)], axis=1)

# Соединяем отфильтрованные заказы с отфильтрованными продажами
merged_data = pd.merge(orders_exploded, sales_filtered, on=['order_id', 'product_id'])

# Группируем и готовим данные для регрессионного анализа
merged_data['order_date'] = pd.to_datetime(merged_data['order_date'])
merged_data['month'] = merged_data['order_date'].dt.to_period('M')
monthly_demand = merged_data.groupby(['store_id', 'product_id', 'month']).agg({'count': 'sum'}).reset_index()

# Прогнозирование с помощью линейной регрессии
forecasts = []

for (store_id, product_id), group in monthly_demand.groupby(['store_id', 'product_id']):
    group = group.sort_values('month')
    X = np.arange(len(group)).reshape(-1, 1)  # Используем индексы в качестве значений X
    y = group['count'].values

    # Создаем и тренируем модель линейной регрессии
    model = LinearRegression()
    model.fit(X, y)

    # Прогноз на следующий месяц
    next_month_index = len(group)
    predicted_count = model.predict([[next_month_index]])[0]

    forecasts.append({
        'store_id': store_id,
        'product_id': product_id,
        'predicted_count': predicted_count
    })

# Преобразуем прогнозы в DataFrame
forecast_df = pd.DataFrame(forecasts)

# Вывод таблицы с результатами
print(forecast_df)

# Чтобы пользователю было удобнее работать с полученными результатами,
# кроме вывода в консоль я сохраню таблицу с результатами в CSV файл
forecast_df.to_csv('forecast_optimal_quantity_of_goods_results.csv', index=False)
