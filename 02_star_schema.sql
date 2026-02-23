USE DATABASE energy_dw;
USE SCHEMA analytics;

CREATE TABLE dim_department (
    department_id INT AUTOINCREMENT PRIMARY KEY,
    department_name STRING
);

CREATE TABLE dim_building (
    building_id INT AUTOINCREMENT PRIMARY KEY,
    site_name STRING,
    building_type STRING,
    building_area FLOAT,
    address STRING,
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE dim_year (
    year_id INT AUTOINCREMENT PRIMARY KEY,
    year INT
);

CREATE TABLE fact_energy (
    fact_id INT AUTOINCREMENT PRIMARY KEY,
    department_name STRING,
    site_name STRING,
    year INT,
    electric_utility STRING,
    electricity_usage FLOAT,
    peak_demand FLOAT,
    natural_gas_usage FLOAT,
    energy_use_intensity FLOAT,
    solar_flag INT
);
