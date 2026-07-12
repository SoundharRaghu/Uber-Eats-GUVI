-- ============================================
-- Uber Eats Bangalore Restaurant Intelligence
-- Author: Raghu Soundhar
-- Total Queries: 15 (10 Restaurant + 5 Order)
-- ============================================

-- ==================================================
-- RESTAURANT QUERIES (10)
-- ==================================================

-- Q1: Top 10 Locations by Average Rating
SELECT location,
       ROUND(AVG(rate), 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY location
HAVING COUNT(*) > 10
ORDER BY avg_rating DESC
LIMIT 10;

-- Q2: Over-saturated Locations
SELECT location,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY location
ORDER BY total_restaurants DESC
LIMIT 10;

-- Q3: Online Order Impact on Ratings
SELECT online_order,
       ROUND(AVG(rate), 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY online_order;

-- Q4: Table Booking Correlation with Ratings
SELECT book_table,
       ROUND(AVG(rate), 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY book_table;

-- Q5: Best Price Segment by Rating
SELECT price_segment,
       ROUND(AVG(rate), 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY price_segment
ORDER BY avg_rating DESC;

-- Q6: Price Segment Deep Dive (Rating + Cost)
SELECT price_segment,
       ROUND(AVG(rate), 2) AS avg_rating,
       ROUND(AVG(cost), 2) AS avg_cost,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY price_segment;

-- Q7: Most Common Cuisines
SELECT cuisines,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY cuisines
ORDER BY total_restaurants DESC
LIMIT 10;

-- Q8: Top-Rated Cuisines (Statistically Significant)
SELECT cuisines,
       ROUND(AVG(rate), 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY cuisines
HAVING COUNT(*) > 20
ORDER BY avg_rating DESC
LIMIT 10;

-- Q9: Cost vs Rating Relationship (Bucketed)
SELECT
    CASE
        WHEN cost < 300 THEN 'under 300'
        WHEN cost BETWEEN 300 AND 700 THEN '300-700'
        ELSE 'Above 700'
    END AS cost_bucket,
    ROUND(AVG(rate), 2) AS avg_rating,
    COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY cost_bucket;

-- Q10: High-Demand Areas Needing Quality Improvement
SELECT location,
       COUNT(*) AS demand,
       ROUND(AVG(rate), 2) AS avg_rating
FROM restaurants
GROUP BY location
HAVING COUNT(*) > 50 AND AVG(rate) < 4.0
ORDER BY demand DESC
LIMIT 5;

-- ==================================================
-- ORDER QUERIES (5 - Custom)
-- ==================================================

-- OQ1: Top 10 Revenue-Generating Restaurants
SELECT restaurant_name,
       ROUND(SUM(order_value), 2) AS total_revenue,
       COUNT(*) AS total_orders
FROM orders
GROUP BY restaurant_name
ORDER BY total_revenue DESC
LIMIT 10;

-- OQ2: Discount Impact on Order Value
SELECT discount_used,
       ROUND(AVG(order_value), 2) AS avg_order_value,
       COUNT(*) AS total_orders,
       ROUND(SUM(order_value), 2) AS total_revenue
FROM orders
GROUP BY discount_used;

-- OQ3: Payment Method Preferences
SELECT payment_method,
       COUNT(*) AS total_orders,
       ROUND(SUM(order_value), 2) AS total_revenue,
       ROUND(AVG(order_value), 2) AS avg_order_value
FROM orders
GROUP BY payment_method
ORDER BY total_orders DESC;

-- OQ4: Monthly Revenue Trend
SELECT year, month, month_name,
       COUNT(*) AS orders,
       ROUND(SUM(order_value), 2) AS revenue,
       ROUND(AVG(order_value), 2) AS avg_order
FROM orders
GROUP BY year, month
ORDER BY year, month;

-- OQ5: Customer Loyalty (Most Repeat Orders)
SELECT restaurant_name,
       COUNT(*) AS repeat_orders,
       ROUND(AVG(order_value), 2) AS avg_order_value,
       ROUND(SUM(order_value), 2) AS total_revenue
FROM orders
GROUP BY restaurant_name
ORDER BY repeat_orders DESC
LIMIT 10;