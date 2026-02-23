CREATE ROLE analyst_role;

GRANT USAGE ON DATABASE energy_dw TO ROLE analyst_role;
GRANT USAGE ON SCHEMA analytics TO ROLE analyst_role;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO ROLE analyst_role;

CREATE USER analyst_user
PASSWORD='StrongPassword@123'
DEFAULT_ROLE=analyst_role;

GRANT ROLE analyst_role TO USER analyst_user;
