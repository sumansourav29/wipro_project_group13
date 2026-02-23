from utils.db_connection import get_connection

def load(df):

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO fact_energy (
            department_name,
            site_name,
            year,
            electric_utility,
            electricity_usage,
            peak_demand,
            natural_gas_usage,
            energy_use_intensity,
            solar_flag
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row["department_name"],
            row["site_name"],
            int(row["year"]),
            row["electric_utility"],
            float(row["electricity_usage"]),
            float(row["peak_demand"]),
            float(row["natural_gas_usage"]),
            float(row["energy_use_intensity"]),
            int(row["solar_flag"])
        ))

    conn.commit()
    cursor.close()
    conn.close()
