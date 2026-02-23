def transform(df):

    df = df.fillna(0)

    df["solar_flag"] = df["Current Solar"].apply(
        lambda x: 1 if x > 0 else 0
    )

    df = df.rename(columns={
        "Department": "department_name",
        "Site Name": "site_name",
        "Year": "year",
        "Electric Utility": "electric_utility",
        "Electricity Usage": "electricity_usage",
        "Peak Electric Demand": "peak_demand",
        "Natural Gas Usage": "natural_gas_usage",
        "Energy Use Intensity": "energy_use_intensity"
    })

    return df
