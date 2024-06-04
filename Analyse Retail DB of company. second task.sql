-- Файл написал на языке PostgreSQL

-- CTE для разворачивания массива JSON с информацией о товарах в заказах
WITH expanded_orders AS (
    SELECT 
        order_id, order_date, user_id,
        json_array_elements(product_info::json) AS product_info
    FROM 
        orders
),

-- CTE только для принятых и не отмененных продаж
filtered_sales AS (
    SELECT
        order_id, product_id
    FROM
        sales
    WHERE
        is_accepted = true AND is_canceled = false
),

-- CTE для вычисления сумм и выручки по продуктам в заказах извлекаем из JSON-массива product_info
revenue_calculations AS (
    SELECT
        eo.order_id,
        eo.order_date,
        eo.user_id,
        (eo.product_info->>'product_id')::int AS product_id,
        (eo.product_info->>'product_price')::numeric AS product_price,
        (
            CASE 
                WHEN (eo.product_info->>'comission_is_percent')::boolean = true 
                THEN (eo.product_info->>'product_price')::numeric * (eo.product_info->>'product_comission')::numeric / 100 
                ELSE (eo.product_info->>'product_comission')::numeric 
            END
        ) * (eo.product_info->>'count')::numeric AS commission,
        (eo.product_info->>'count')::int AS count
    FROM
        expanded_orders eo
    JOIN 
        filtered_sales fs ON eo.order_id = fs.order_id 
                         AND (eo.product_info->>'product_id')::int = fs.product_id
)


-- Итоговый SELECT для агрегации данных по пользователям и заказам
SELECT
    u.user_id AS USER_ID,
    rc.order_id AS ORDER_ID,
    rc.order_date AS ORDER_DATE,
    SUM(rc.product_price * rc.count) AS ORDER_SUM,
    SUM(rc.commission) AS ORDER_REVENUE,
    SUM(rc.count) AS ORDER_QUANTITY,
    COUNT(DISTINCT rc.product_id) AS ORDER_UNIQUE_PRODUCTS
FROM
    revenue_calculations rc
JOIN
    "user" u ON rc.user_id = u.user_id
GROUP BY
    u.user_id, 
    rc.order_id, 
    rc.order_date
ORDER BY
    u.user_id, 
    rc.order_date;