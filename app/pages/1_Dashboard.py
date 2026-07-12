import streamlit as st
import pandas as pd
import sqlite3

# =========================================
# Page Setup
# =========================================
st.title("Restaurant Dashboard")
st.markdown("Filter restaurants dynamically using SQL")
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


# =========================================
# Load Filter Options from Database
# =========================================
@st.cache_data
def get_filter_options():
    locations = pd.read_sql_query(
        "SELECT DISTINCT location FROM restaurants ORDER BY location",
        conn
    )['location'].tolist()
    return locations


locations = get_filter_options()


# =========================================
# Sidebar Filters
# =========================================
st.sidebar.header("Filters")

loc = st.sidebar.multiselect(
    "Location (select one or more)",
    locations
)

online = st.sidebar.radio(
    "Online Order",
    ['All', 'Yes', 'No'],
    horizontal=True
)

book = st.sidebar.radio(
    "Table Booking",
    ['All', 'Yes', 'No'],
    horizontal=True
)

price_seg = st.sidebar.multiselect(
    "Price Segment",
    ['Low', 'Medium', 'Premium'],
    default=['Low', 'Medium', 'Premium']
)

cost_range = st.sidebar.slider(
    "Cost Range (Rs)",
    0, 5000, (100, 2000)
)

rating_min = st.sidebar.slider(
    "Minimum Rating",
    0.0, 5.0, 3.0, 0.1
)


# =========================================
# Build Dynamic SQL Query
# =========================================
query = """
SELECT name, location, cuisines, rate, cost,
       price_segment, online_order, book_table
FROM restaurants
WHERE 1=1
"""

if loc:
    loc_list = "','".join(loc)
    query += f" AND location IN ('{loc_list}')"

if online != 'All':
    query += f" AND online_order = '{online}'"

if book != 'All':
    query += f" AND book_table = '{book}'"

if price_seg:
    seg_list = "','".join(price_seg)
    query += f" AND price_segment IN ('{seg_list}')"

query += f" AND cost BETWEEN {cost_range[0]} AND {cost_range[1]}"
query += f" AND rate >= {rating_min}"
query += " ORDER BY rate DESC LIMIT 100"


# =========================================
# Execute Query and Display Results
# =========================================
try:
    result = pd.read_sql_query(query, conn)

    if len(result) == 0:
        st.warning("No restaurants match your filters. Try relaxing them.")
    else:
        st.success(f"Found {len(result)} restaurants (showing top 100)")
        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )
except Exception as e:
    st.error(f"Query error: {str(e)}")