import snowflake.connector
import streamlit as st

def get_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["SF_USER"],
        password=st.secrets["SF_PASSWORD"],
        account=st.secrets["SF_ACCOUNT"],
    )

    # Force everything from Python side
    cursor = conn.cursor()
    cursor.execute("USE ROLE ACCOUNTADMIN")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    cursor.execute("USE DATABASE ENERGY_DW")
    cursor.execute("USE SCHEMA ANALYTICS")

    return conn
