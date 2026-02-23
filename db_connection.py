import snowflake.connector
import streamlit as st

def get_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["SF_USER"],
        password=st.secrets["SF_PASSWORD"],
        account=st.secrets["SF_ACCOUNT"],
        warehouse="energy_wh"
    )

    conn.cursor().execute("USE DATABASE energy_dw")
    conn.cursor().execute("USE SCHEMA analytics")

    return conn
