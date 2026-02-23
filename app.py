import streamlit as st
import pandas as pd
from db_connection import get_connection

st.set_page_config(
    page_title="Energy Consumption Dashboard",
    layout="wide"
)

st.title("⚡ Energy Consumption Monitoring Dashboard")

# -----------------------------------
# Database Connection
# -----------------------------------
try:
    conn = get_connection()
except Exception as e:
    st.error("❌ Database Connection Failed")
    st.error(str(e))
    st.stop()

# -----------------------------------
# Yearly Electricity Usage
# -----------------------------------
st.subheader("📊 Yearly Electricity Usage")

query_yearly = """
SELECT year, SUM(electricity_usage) AS total_usage
FROM fact_energy
GROUP BY year
ORDER BY year
"""

try:
    df_yearly = pd.read_sql(query_yearly, conn)

    if df_yearly.empty:
        st.warning("No data found in fact_energy table.")
    else:
        df_yearly.columns = df_yearly.columns.str.upper()
        st.line_chart(df_yearly.set_index("YEAR"))

except Exception as e:
    st.error("Error fetching yearly data")
    st.error(str(e))


# -----------------------------------
# Utility-wise Usage
# -----------------------------------
st.subheader("🏢 Electricity Usage by Utility")

query_utility = """
SELECT electric_utility,
       SUM(electricity_usage) AS total_usage
FROM fact_energy
GROUP BY electric_utility
ORDER BY total_usage DESC
"""

try:
    df_utility = pd.read_sql(query_utility, conn)

    if not df_utility.empty:
        df_utility.columns = df_utility.columns.str.upper()
        st.bar_chart(df_utility.set_index("ELECTRIC_UTILITY"))

except Exception as e:
    st.error("Error fetching utility data")
    st.error(str(e))


# -----------------------------------
# Top 10 Buildings
# -----------------------------------
st.subheader("🏆 Top 10 Buildings by Electricity Usage")

query_top = """
SELECT site_name,
       SUM(electricity_usage) AS total_usage
FROM fact_energy
GROUP BY site_name
ORDER BY total_usage DESC
LIMIT 10
"""

try:
    df_top = pd.read_sql(query_top, conn)

    if not df_top.empty:
        st.dataframe(df_top)

except Exception as e:
    st.error("Error fetching ranking data")
    st.error(str(e))


# Close Connection
conn.close()
