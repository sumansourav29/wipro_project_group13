import streamlit as st
import pandas as pd
import os
import altair as alt
from db_connection import get_connection
from snowflake.connector.pandas_tools import write_pandas

st.set_page_config(page_title="Energy Consumption Dashboard", layout="wide")
st.title("⚡ Energy Consumption Monitoring Dashboard")


# --------------------------------------------------
# Auto Load CSV If Table Is Empty
# --------------------------------------------------
def load_csv_if_empty(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM FACT_ENERGY")
    count = cursor.fetchone()[0]

    if count == 0:
        st.info("Loading dataset into Snowflake...")

        file_path = os.path.join(os.getcwd(), "energy_consumption_dataset.csv")

        df = pd.read_csv(file_path = "energy_consumption_dataset.csv")
        df.columns = df.columns.str.strip()
        df = df.fillna(0)

        # Clean Year
        df["YEAR"] = (
            df["Year"]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
        df = df.dropna(subset=["YEAR"])

        df["SOLAR_FLAG"] = df["Current Solar"].apply(lambda x: 1 if x > 0 else 0)

        df = df.rename(columns={
            "Department": "DEPARTMENT_NAME",
            "Site Name": "SITE_NAME",
            "Electric Utility": "ELECTRIC_UTILITY",
            "Electricity Usage": "ELECTRICITY_USAGE",
            "Peak Electric Demand": "PEAK_DEMAND",
            "Natural Gas Usage": "NATURAL_GAS_USAGE",
            "Energy Use Intensity": "ENERGY_USE_INTENSITY"
        })

        df = df[[
            "DEPARTMENT_NAME",
            "SITE_NAME",
            "YEAR",
            "ELECTRIC_UTILITY",
            "ELECTRICITY_USAGE",
            "PEAK_DEMAND",
            "NATURAL_GAS_USAGE",
            "ENERGY_USE_INTENSITY",
            "SOLAR_FLAG"
        ]]

        write_pandas(conn, df, "FACT_ENERGY")
        st.success("Dataset successfully loaded!")

    cursor.close()


# --------------------------------------------------
# Connect to Snowflake
# --------------------------------------------------
try:
    conn = get_connection()
    load_csv_if_empty(conn)
except Exception as e:
    st.error("❌ Database Connection Failed")
    st.error(str(e))
    st.stop()


# --------------------------------------------------
# 📊 Yearly Electricity Usage
# --------------------------------------------------
st.subheader("📊 Yearly Electricity Usage")

query_yearly = """
SELECT YEAR,
       SUM(ELECTRICITY_USAGE) AS TOTAL_USAGE
FROM FACT_ENERGY
WHERE YEAR IS NOT NULL
GROUP BY YEAR
ORDER BY YEAR
"""

try:
    df_yearly = pd.read_sql(query_yearly, conn)

    if df_yearly.empty:
        st.warning("No valid yearly data found.")
    else:
        # Clean Year column from Snowflake
        df_yearly["YEAR"] = (
            df_yearly["YEAR"]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df_yearly["YEAR"] = pd.to_numeric(df_yearly["YEAR"], errors="coerce")
        df_yearly = df_yearly.dropna()
        df_yearly = df_yearly.sort_values("YEAR")

        chart = alt.Chart(df_yearly).mark_line(point=True).encode(
            x=alt.X("YEAR:O", title="Year"),
            y=alt.Y("TOTAL_USAGE:Q", title="Total Electricity Usage"),
            tooltip=["YEAR", "TOTAL_USAGE"]
        ).properties(height=400)

        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error("Error fetching yearly data")
    st.error(str(e))


# --------------------------------------------------
# 🏢 Utility-wise Usage
# --------------------------------------------------
st.subheader("🏢 Electricity Usage by Utility")

query_utility = """
SELECT ELECTRIC_UTILITY,
       SUM(ELECTRICITY_USAGE) AS TOTAL_USAGE
FROM FACT_ENERGY
GROUP BY ELECTRIC_UTILITY
ORDER BY TOTAL_USAGE DESC
"""

try:
    df_utility = pd.read_sql(query_utility, conn)

    if not df_utility.empty:
        chart2 = alt.Chart(df_utility).mark_bar().encode(
            x=alt.X("ELECTRIC_UTILITY:O", title="Utility"),
            y=alt.Y("TOTAL_USAGE:Q", title="Total Usage"),
            tooltip=["ELECTRIC_UTILITY", "TOTAL_USAGE"]
        ).properties(height=400)

        st.altair_chart(chart2, use_container_width=True)

except Exception as e:
    st.error("Error fetching utility data")
    st.error(str(e))


# --------------------------------------------------
# 🏆 Top 10 Buildings
# --------------------------------------------------
st.subheader("🏆 Top 10 Buildings by Electricity Usage")

query_top = """
SELECT SITE_NAME,
       SUM(ELECTRICITY_USAGE) AS TOTAL_USAGE
FROM FACT_ENERGY
GROUP BY SITE_NAME
ORDER BY TOTAL_USAGE DESC
LIMIT 10
"""

try:
    df_top = pd.read_sql(query_top, conn)

    if not df_top.empty:
        st.dataframe(df_top)

except Exception as e:
    st.error("Error fetching ranking data")
    st.error(str(e))


conn.close()
