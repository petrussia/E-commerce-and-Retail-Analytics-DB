import json


# Функция для расчета прибыли 1 заказа
def calculate_profit(row):
    product_info = json.loads(row['product_info'])
    for product in product_info:
        if product['product_id'] == row['product_id']:
            product_price = product['product_price']
            if product['comission_is_percent']:
                profit = product_price * (product['product_comission'] / 100) * product['count']
            else:
                profit = product['product_comission'] * product['count']
            return profit
    return 0


# Функция для расчета выручки с одного заказа
def calculate_sale_amount(row):
    product_info = json.loads(row['product_info'])
    for product in product_info:
        if product['product_id'] == row['product_id']:
            return product['product_price'] * product['count']
    return 0
