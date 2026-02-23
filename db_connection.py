import snowflake.connector
import streamlit as st

def get_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["SF_USER"],
        password=st.secrets["SF_PASSWORD"],
        account=st.secrets["SF_ACCOUNT"],
        warehouse="COMPUTE_WH",
        database="ENERGY_DW",
        schema="ANALYTICS"
    )
    return conn
