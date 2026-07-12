import streamlit as st
import pandas as pd
import sqlite3

# =========================================
# Page Setup
# =========================================
st.title("Order Analytics")
st.markdown("Custom order insights based on JSON order data (5 questions)")
st.markdown("---")


# =========================================
# Database Connection
# =========================================
@st.cache_resource
def get_connection():
    return sqlite3.connect(
        '../database/ubereats.db',
        check_same_thread=False
    )


conn = get_connection()


def run_query(sql):
    return pd.read_sql_query(sql, conn)


# =========================================
# OQ1: Top Revenue Restaurants
# =========================================
with st.expander("OQ1: Which restaurants generate the highest revenue?"):
    st.markdown("**Business Value:** Identifies top-earning partners for VIP treatment programs.")
    oq1 = """
    SELECT restaurant_name,
           ROUND(SUM(order_value), 2) AS total_revenue,
           COUNT(*) AS total_orders
    FROM orders
    GROUP BY restaurant_name
    ORDER BY total_revenue DESC
    LIMIT 10;
    """
    st.dataframe(run_query(oq1), use_container_width=True, hide_index=True)


# =========================================
# OQ2: Discount Impact
# =========================================
with st.expander("OQ2: Do discounts drive higher order values or increase frequency?"):
    st.markdown("**Business Value:** Validates discount strategy effectiveness.")
    oq2 = """
    SELECT discount_used,
           ROUND(AVG(order_value), 2) AS avg_order_value,
           COUNT(*) AS total_orders,
           ROUND(SUM(order_value), 2) AS total_revenue
    FROM orders
    GROUP BY discount_used;
    """
    st.dataframe(run_query(oq2), use_container_width=True, hide_index=True)


# =========================================
# OQ3: Payment Method Preferences
# =========================================
with st.expander("OQ3: Which payment method is most popular?"):
    st.markdown("**Business Value:** Prioritize payment integrations based on customer usage.")
    oq3 = """
    SELECT payment_method,
           COUNT(*) AS total_orders,
           ROUND(SUM(order_value), 2) AS total_revenue,
           ROUND(AVG(order_value), 2) AS avg_order_value
    FROM orders
    GROUP BY payment_method
    ORDER BY total_orders DESC;
    """
    st.dataframe(run_query(oq3), use_container_width=True, hide_index=True)


# =========================================
# OQ4: Monthly Revenue Trend
# =========================================
with st.expander("OQ4: How does the monthly revenue trend look?"):
    st.markdown("**Business Value:** Identifies growth patterns and seasonal opportunities.")
    oq4 = """
    SELECT year, month, month_name,
           COUNT(*) AS orders,
           ROUND(SUM(order_value), 2) AS revenue,
           ROUND(AVG(order_value), 2) AS avg_order
    FROM orders
    GROUP BY year, month
    ORDER BY year, month;
    """
    st.dataframe(run_query(oq4), use_container_width=True, hide_index=True)


# =========================================
# OQ5: Customer Loyalty
# =========================================
with st.expander("OQ5: Which restaurants have the most repeat orders (customer loyalty)?"):
    st.markdown("**Business Value:** Identifies model partners with sticky customer bases.")
    oq5 = """
    SELECT restaurant_name,
           COUNT(*) AS repeat_orders,
           ROUND(AVG(order_value), 2) AS avg_order_value,
           ROUND(SUM(order_value), 2) AS total_revenue
    FROM orders
    GROUP BY restaurant_name
    ORDER BY repeat_orders DESC
    LIMIT 10;
    """
    st.dataframe(run_query(oq5), use_container_width=True, hide_index=True)