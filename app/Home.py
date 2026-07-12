import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Uber Eats Banglore",
    layout="wide",
    page_icon="🍔"
)
st.title("Uber Eats Bangalore restaurant Intelligence")
st.markdown("### GUVI Data Science Capstone by Soundhar Raghu")
st.markdown("---")

@st.cache_data
def load_kpis():
    conn = sqlite3.connect('../database/ubereats.db')

    total_rest=pd.read_sql_query("SELECT COUNT(*) FROM restaurants", conn).iloc[0,0]
    
    total_loc=pd.read_sql_query("SELECT COUNT(DISTINCT location) FROM restaurants", conn).iloc[0,0]

    total_cuisines=pd.read_sql_query("SELECT COUNT(DISTINCT cuisines) FROM restaurants", conn).iloc[0,0]

    total_orders=pd.read_sql_query("SELECT COUNT(*) FROM orders", conn).iloc[0,0]

    total_revenue=pd.read_sql_query("SELECT SUM(order_value) FROM orders",conn).iloc[0,0]

    conn.close()
    return total_rest,total_loc,total_cuisines,total_orders,total_revenue

rest,loc,cuis,orders,revenue = load_kpis()

st.subheader("Restaurant Metrics")

col1,col2,col3 = st.columns(3)
col1.metric("Total restaurants",f"{rest:,}")
col2.metric("Unique Location", loc)
col3.metric("Unique Cuisines", cuis)

st.subheader("Order Metrics")

col4,col5,col6 = st.columns(3)
col4.metric("Total Orders",f"{orders:,}")
col5.metric("Total Revenue",f"Rs{revenue:,.0f}")
col6.metric("Avg Order Value",f"Rs{revenue/orders:,.0f}")

st.markdown("---")
st.info("Navigate to pages on the LEFT SIDEBAR for detailed analysis")

