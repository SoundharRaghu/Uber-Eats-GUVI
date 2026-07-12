import streamlit as st
import pandas as pd
import sqlite3

# =========================================
# Page Setup
# =========================================
st.title("Business Q&A")
st.markdown("10 predefined business questions with SQL-based answers")
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
# Q1: Top Locations by Rating
# =========================================
with st.expander("Q1: Which Bangalore locations have the highest average restaurant ratings?"):
    st.markdown("**Business Value:** Identifies premium areas for brand positioning and partner onboarding.")
    q1 = """
    SELECT location,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY location
    HAVING COUNT(*) > 10
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
    st.dataframe(run_query(q1), use_container_width=True, hide_index=True)


# =========================================
# Q2: Over-saturated Locations
# =========================================
with st.expander("Q2: Which locations are over-saturated with restaurants?"):
    st.markdown("**Business Value:** Helps avoid overcrowded markets and guides expansion decisions.")
    q2 = """
    SELECT location,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY location
    ORDER BY total_restaurants DESC
    LIMIT 10;
    """
    st.dataframe(run_query(q2), use_container_width=True, hide_index=True)


# =========================================
# Q3: Online Order Impact
# =========================================
with st.expander("Q3: Does online ordering improve restaurant ratings?"):
    st.markdown("**Business Value:** Evaluates ROI of Uber Eats online ordering feature.")
    q3 = """
    SELECT online_order,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY online_order;
    """
    st.dataframe(run_query(q3), use_container_width=True, hide_index=True)


# =========================================
# Q4: Table Booking Impact
# =========================================
with st.expander("Q4: Does table booking correlate with higher customer ratings?"):
    st.markdown("**Business Value:** Measures effectiveness of table booking as a premium feature.")
    q4 = """
    SELECT book_table,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY book_table;
    """
    st.dataframe(run_query(q4), use_container_width=True, hide_index=True)


# =========================================
# Q5: Best Price Segment
# =========================================
with st.expander("Q5: What price range delivers the best customer satisfaction?"):
    st.markdown("**Business Value:** Helps define optimal pricing segment for partner success.")
    q5 = """
    SELECT price_segment,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY price_segment
    ORDER BY avg_rating DESC;
    """
    st.dataframe(run_query(q5), use_container_width=True, hide_index=True)


# =========================================
# Q6: Price Segment Deep Dive
# =========================================
with st.expander("Q6: How do Low, Mid, and Premium restaurants perform in terms of ratings?"):
    st.markdown("**Business Value:** Supports pricing-based market segmentation strategies.")
    q6 = """
    SELECT price_segment,
           ROUND(AVG(rate), 2) AS avg_rating,
           ROUND(AVG(cost), 2) AS avg_cost,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY price_segment;
    """
    st.dataframe(run_query(q6), use_container_width=True, hide_index=True)


# =========================================
# Q7: Most Common Cuisines
# =========================================
with st.expander("Q7: Which cuisines are most common in Bangalore?"):
    st.markdown("**Business Value:** Reveals market demand and cuisine saturation.")
    q7 = """
    SELECT cuisines,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY cuisines
    ORDER BY total_restaurants DESC
    LIMIT 10;
    """
    st.dataframe(run_query(q7), use_container_width=True, hide_index=True)


# =========================================
# Q8: Top-Rated Cuisines
# =========================================
with st.expander("Q8: Which cuisines receive the highest average ratings?"):
    st.markdown("**Business Value:** Identifies high-quality cuisine categories suitable for promotion.")
    q8 = """
    SELECT cuisines,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY cuisines
    HAVING COUNT(*) > 20
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
    st.dataframe(run_query(q8), use_container_width=True, hide_index=True)


# =========================================
# Q9: Cost vs Rating Relationship
# =========================================
with st.expander("Q9: What is the relationship between restaurant cost and rating?"):
    st.markdown("**Business Value:** Determines if higher pricing translates to better customer perception.")
    q9 = """
    SELECT
        CASE
            WHEN cost < 300 THEN 'Under 300'
            WHEN cost BETWEEN 300 AND 700 THEN '300-700'
            ELSE 'Above 700'
        END AS cost_bucket,
        ROUND(AVG(rate), 2) AS avg_rating,
        COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY cost_bucket;
    """
    st.dataframe(run_query(q9), use_container_width=True, hide_index=True)


# =========================================
# Q10: High Demand, Low Rating
# =========================================
with st.expander("Q10: Which locations show high demand but lower average ratings?"):
    st.markdown("**Business Value:** Indicates areas where quality improvement is needed.")
    q10 = """
    SELECT location,
           COUNT(*) AS demand,
           ROUND(AVG(rate), 2) AS avg_rating
    FROM restaurants
    GROUP BY location
    HAVING COUNT(*) > 50 AND AVG(rate) < 4.0
    ORDER BY demand DESC
    LIMIT 5;
    """
    st.dataframe(run_query(q10), use_container_width=True, hide_index=True)