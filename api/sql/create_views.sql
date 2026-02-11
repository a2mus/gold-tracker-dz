-- Materialized view for latest gold prices by karat
CREATE OR REPLACE VIEW latest_gold_prices AS
SELECT 
    karat,
    (buy_price + sell_price) / 2 AS current_price,
    buy_price,
    sell_price,
    timestamp AS last_updated,
    'calculated' AS source
FROM (
    SELECT DISTINCT ON (karat) 
        karat,
        FIRST_VALUE(buy_price) OVER (PARTITION BY karat ORDER BY timestamp DESC) AS buy_price,
        FIRST_VALUE(sell_price) OVER (PARTITION BY karat ORDER BY timestamp DESC) AS sell_price,
        FIRST_VALUE(timestamp) OVER (PARTITION BY karat ORDER BY timestamp DESC) AS timestamp
    FROM gold_prices
    WHERE karat IN (18, 21, 22, 24)
) subquery;

-- Historical price data for charts (daily averages)
CREATE OR REPLACE VIEW historical_gold_prices_daily AS
SELECT 
    karat,
    DATE_TRUNC('day', timestamp) AS date,
    AVG((buy_price + sell_price) / 2) AS avg_price,
    MIN(buy_price) AS min_buy,
    MAX(buy_price) AS max_buy,
    MIN(sell_price) AS min_sell,
    MAX(sell_price) AS max_sell,
    COUNT(*) AS data_points
FROM gold_prices
WHERE karat IN (18, 21, 22, 24)
  AND timestamp >= NOW() - INTERVAL '30 days'
GROUP BY karat, DATE_TRUNC('day', timestamp)
ORDER BY karat, date DESC;

-- Hourly price data for detailed charts
CREATE OR REPLACE VIEW gold_prices_hourly AS
SELECT 
    karat,
    DATE_TRUNC('hour', timestamp) AS hour,
    AVG((buy_price + sell_price) / 2) AS avg_price,
    COUNT(*) AS data_points
FROM gold_prices
WHERE karat IN (18, 21, 22, 24)
  AND timestamp >= NOW() - INTERVAL '7 days'
GROUP BY karat, DATE_TRUNC('hour', timestamp)
ORDER BY karat, hour DESC;
