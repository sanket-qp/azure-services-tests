
CREATE SCHEMA ${appfunc}_schema;
 
/* Allow users to connect to the database. */
GRANT CONNECT ON DATABASE ${appname}_db TO wf_${appname}_pg_app_ddl_user;
GRANT CONNECT ON DATABASE ${appname}_db TO wf_${appname}_pg_app_dml_user;
GRANT CONNECT ON DATABASE ${appname}_db TO wf_${appname}_pg_app_dql_user;
 
/* Make sure public role cannot do anything with the schema. */
REVOKE CREATE ON SCHEMA ${appfunc}_schema FROM PUBLIC;
REVOKE ALL ON DATABASE ${appname}_db FROM PUBLIC;
 
/* DDL user owns the schema. */
ALTER SCHEMA ${appfunc}_schema OWNER TO wf_${appname}_pg_app_ddl_role;
 
/* Set the seach path to the database. Tables and other objects in a schema
   can always by referred to like ${appfunc}_schema.table, but setting the
   search path allows referring to the table as just 'table'. */
ALTER DATABASE ${appfunc}_db SET SEARCH_PATH TO ${appfunc}_schema;
 
/* Allow DDL role to use and create objects in schema. */
GRANT USAGE, CREATE ON SCHEMA ${appfunc}_schema TO wf_${appname}_pg_app_ddl_role;
 
/* Set permissions for DML role, allowing use of the schema, and data
   management operations in the schema. */
GRANT USAGE ON SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml_role;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml_role;
GRANT EXECUTE ON ALL ROUTINES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml_role;
 
/* Grant default privileges to apply to future created objects. */
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO
    wf_${appname}_pg_app_dml_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO wf_${appname}_pg_app_dml_role;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl_role IN SCHEMA ${appfunc}_schema
    GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO
    wf_${appname}_pg_app_dml_role;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl_role IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO
    wf_${appname}_pg_app_dml_role;
 
/* Set permissions for DQL role, allowing use of the schema, and selecting
   from tables, both exisitng tables and tables created in the future. */
GRANT USAGE ON SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql_role;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql_role;
GRANT EXECUTE ON ALL ROUTINES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql_role;
GRANT SELECT ON ALL TABLES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql_role;
 
/* Drant default privileges to apply to future created objects. */
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT SELECT ON TABLES TO
    wf_${appname}_pg_app_dql_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO wf_${appname}_pg_app_dql_role;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl_role IN SCHEMA ${appfunc}_schema
    GRANT SELECT ON TABLES TO
    wf_${appname}_pg_app_dql_role;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl_role IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO
    wf_${appname}_pg_app_dql_role;
