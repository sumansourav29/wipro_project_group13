import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

st.set_page_config(layout="wide")
st.title("⚡ Energy Consumption Monitoring Dashboard")

conn = get_connection()

query1 = """
SELECT year, SUM(electricity_usage) AS total_usage
FROM fact_energy
GROUP BY year
ORDER BY year
"""

df1 = pd.read_sql(query1, conn)

st.subheader("Yearly Electricity Usage")
st.line_chart(df1.set_index("YEAR"))

query2 = """
SELECT electric_utility, SUM(electricity_usage) AS total_usage
FROM fact_energy
GROUP BY electric_utility
ORDER BY total_usage DESC
"""

df2 = pd.read_sql(query2, conn)

st.subheader("Utility-wise Usage")
st.bar_chart(df2.set_index("ELECTRIC_UTILITY"))

conn.close()
