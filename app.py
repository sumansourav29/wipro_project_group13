def load_csv_if_empty(conn):
    import pandas as pd

    check_query = "SELECT COUNT(*) FROM FACT_ENERGY"
    count = pd.read_sql(check_query, conn).iloc[0, 0]

    if count == 0:
        df = pd.read_csv("energy_consumption_dataset.csv")
        df.columns = df.columns.str.strip()

        df["solar_flag"] = df["Current Solar"].apply(lambda x: 1 if x > 0 else 0)

        df = df.rename(columns={
            "Department": "DEPARTMENT_NAME",
            "Site Name": "SITE_NAME",
            "Year": "YEAR",
            "Electric Utility": "ELECTRIC_UTILITY",
            "Electricity Usage": "ELECTRICITY_USAGE",
            "Peak Electric Demand": "PEAK_DEMAND",
            "Natural Gas Usage": "NATURAL_GAS_USAGE",
            "Energy Use Intensity": "ENERGY_USE_INTENSITY"
        })

        insert_query = """
        INSERT INTO FACT_ENERGY
        (DEPARTMENT_NAME, SITE_NAME, YEAR, ELECTRIC_UTILITY,
         ELECTRICITY_USAGE, PEAK_DEMAND, NATURAL_GAS_USAGE,
         ENERGY_USE_INTENSITY, SOLAR_FLAG)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row["DEPARTMENT_NAME"],
                row["SITE_NAME"],
                int(row["YEAR"]),
                row["ELECTRIC_UTILITY"],
                float(row["ELECTRICITY_USAGE"]),
                float(row["PEAK_DEMAND"]),
                float(row["NATURAL_GAS_USAGE"]),
                float(row["ENERGY_USE_INTENSITY"]),
                int(row["solar_flag"])
            ))

        conn.commit()
        cursor.close()
