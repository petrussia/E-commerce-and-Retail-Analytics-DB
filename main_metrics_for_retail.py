# основной скрипт для задания 3.1
import pandas as pd
import matplotlib.pyplot as plt
from calculation_functions import calculate_profit, calculate_sale_amount
from making_presentation_with_analitics import making_presentation


# Загружаем данные
print("Загружаем данные компании")
orders = pd.read_csv('correct_orders.csv')
sales = pd.read_csv('sales.csv')
store = pd.read_csv('store.csv')
product = pd.read_csv('product.csv')

# Фильтрация продаж
sales_filtered = sales[(sales['is_accepted'] == True) & (sales['is_canceled'] == False)]

# Объединение данных продаж и заказов
merged_data = pd.merge(sales_filtered, orders, on='order_id', how='left')

print("\nВычисляем общие метрики компании")
# Вычисление прибыли и стоимости продажи для каждой строки
merged_data['profit'] = merged_data.apply(calculate_profit, axis=1)
merged_data['sale_amount'] = merged_data.apply(calculate_sale_amount, axis=1)

# Подсчет общей выручки с продаж и количества заказов
total_sales_amount = merged_data['sale_amount'].sum()
total_orders = merged_data['order_id'].nunique()

# Общая сумма прибыли
total_profit = merged_data['profit'].sum()

# Вывод общих метрик по всей сети
print(f"Общая выручка компании: {total_sales_amount}")
print(f"Общая сумма прибыли компании: {total_profit}")
print(f"Количество заказов за всё время: {total_orders}")

print("\nАнализируем клиентов")
# Анализ клиентов
orders_filtered = orders[orders['order_id'].isin(merged_data['order_id'])]
unique_customers = orders_filtered['user_id'].nunique()

print(f"Общее количество уникальных клиентов у компании: {unique_customers}")

print("\nПодготавливаем список самых продаваемых товаров")
# Самые продаваемые товары
top_products = merged_data['product_id'].value_counts().head(10)
top_products_df = top_products.reset_index()
top_products_df.columns = ['product_id', 'Number_of_products']

print("10 самых продаваемых товаров:")
print(top_products_df)

print("\nАнализируем отменённые и возвращённые товары")
# Анализ отменённых и возвращённых товаров
canceled_sales = sales[sales['is_canceled'] == True]
canceled_merged_data = pd.merge(canceled_sales, orders, on='order_id', how='left')
canceled_merged_data['profit'] = canceled_merged_data.apply(calculate_profit, axis=1)
total_cancellations = canceled_sales['order_id'].count()
cancellation_impact = canceled_merged_data['profit'].sum()

print(f"Количество отменённых и возвращённых заказов: {total_cancellations}")
print(f"Влияние отменённых и возвращённых заказов на общую прибыль: {cancellation_impact}")

print("\nСоздаём графики по полученных данным")

# Динамика продаж по дням
merged_data['purchase_date'] = pd.to_datetime(merged_data['purchase_date'])
# Фильтрация данных только по датам до октября 2023 года
end_date = pd.to_datetime('2023-10')
filtered_data = merged_data[merged_data['purchase_date'] < end_date]

# Группировка данных по дням
daily_sales = filtered_data.groupby(filtered_data['purchase_date'].dt.date).size()

# Построение графика динамики продаж по дням
plt.figure(figsize=(10, 6))
daily_sales.plot(kind='line', marker='o')
plt.title('Динамика продаж по дням')
plt.xlabel('Дата')
plt.ylabel('Количество продаж')
plt.grid(True)
plt.savefig('daily_sales_line.png') # сохраняем в файл специально для дальнейшего использования в презентации
plt.show()


# Динамика продаж по месяцам и дням недели
weekly_sales = merged_data.groupby(merged_data['purchase_date'].dt.dayofweek).size()
monthly_sales = merged_data.groupby(merged_data['purchase_date'].dt.month).size()

# Построение круговой диаграммы динамики продаж по 12 месяцам
month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
monthly_sales.index = month
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='viridis')
plt.title('Динамика продаж по 12 месяцам года')
plt.ylabel('')
plt.savefig('monthly_sales_pie.png') # сохраняем в файл специально для дальнейшего использования в презентации
plt.show()

plt.figure(figsize=(10, 6))
weekly_sales.plot(kind='bar')
plt.title('Динамика продаж по дням недели')
plt.xlabel('День недели')
plt.ylabel('Количество продаж')
plt.grid(True)
plt.savefig('weekly_sales_bar.png') # сохраняем в файл специально для дальнейшего использования в презентации
plt.show()

# Динамика прибыли по месяцам
merged_data['purchase_date'] = pd.to_datetime(merged_data['purchase_date'])

# Фильтруем данные только по датам до октября 2023 года
end_date = pd.to_datetime('2023-10-01')
filtered_data = merged_data[merged_data['purchase_date'] < end_date]

# Группируем данные по месяцам и суммируем прибыль
monthly_profit = filtered_data.groupby(filtered_data['purchase_date'].dt.to_period('M'))['profit'].sum()

plt.figure(figsize=(10, 6))
monthly_profit.plot(kind='line', marker='o')
plt.title('Динамика прибыли по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Прибыль')
plt.grid(True)
plt.savefig('monthly_profit_line.png') # сохраняем в файл специально для дальнейшего использования в презентации
plt.show()


print("\nАнализируем магазины сети")
# Анализ магазинов
top_stores_by_profit = merged_data.groupby('store_id')['profit'].sum().nlargest(10)
top_stores_by_sales = merged_data.groupby('store_id')['sale_amount'].sum().nlargest(10)

print("10 магазинов с наибольшей прибылью:")
print(top_stores_by_profit)

print("10 магазинов с наибольшей выручкой:")
print(top_stores_by_sales)

print("\nСохраняем отчёт в формате .csv")
# Сохранение отчета с использованием кодировки 'utf-8'
report_data = {
    'Общая выручка компании': total_sales_amount,
    'Общая сумма прибыли': total_profit,
    'Количество заказов': total_orders,
    'Общее количество уникальных клиентов у компании': unique_customers,
    '10 самых продаваемых товаров': top_products_df.to_dict(orient='records'),
    'Количество отменённых и возвращённых заказов': total_cancellations,
    'Упущенная прибыль отменённых и возвращённых заказов': cancellation_impact,
    'Динамика продаж по месяцам': monthly_sales.to_dict(),
    'Динамика продаж по дням недели': weekly_sales.to_dict(),
    'Динамика прибыли по месяцам': monthly_profit.to_dict(),
    '10 магазинов с наибольшей прибылью': top_stores_by_profit.to_dict(),
    '10 магазинов с наибольшей выручкой': top_stores_by_sales.to_dict()
}

report_df = pd.DataFrame([report_data])
report_df.to_csv('Retails_analytics_of_company_report.csv', index=False, encoding='utf-8')
print("Отчёт можно посмотреть в файле Retails_analytics_of_company_report.csv")
print("\nСоздаём презентацию")
making_presentation( total_sales_amount, total_profit, total_orders, unique_customers, top_products_df, total_cancellations,
cancellation_impact, top_stores_by_profit, top_stores_by_sales )
print("Презентация создана и её можно посмотреть в файле Retail_Analytical_Metrics.pptx")
