CREATE SCHEMA ${appfunc}_schema;

/* Make sure public role cannot do anything with the schema. */
REVOKE CREATE ON SCHEMA ${appfunc}_schema FROM PUBLIC;
REVOKE ALL ON DATABASE ${appfunc}_db FROM PUBLIC;

/* DDL user owns the schema. */
ALTER SCHEMA ${appfunc}_schema OWNER TO wf_${appname}_pg_app_ddl;

/* Allow users to connect to the database. */
GRANT CONNECT ON DATABASE ${appfunc}_db TO wf_${appname}_pg_app_ddl;
GRANT CONNECT ON DATABASE ${appfunc}_db TO wf_${appname}_pg_app_dml;
GRANT CONNECT ON DATABASE ${appfunc}_db TO wf_${appname}_pg_app_dql;
GRANT CONNECT ON DATABASE ${appfunc}_db TO wf_${appname}_pg_ops_readwrite;
GRANT CONNECT ON DATABASE ${appfunc}_db TO wf_${appname}_pg_ops_readonly;

/* Set the seach path to the database. Tables and other objects in a schema
   can always by referred to like ${appfunc}_schema.table, but setting the
   search path allows referring to the table as just 'table'. */
ALTER DATABASE ${appfunc}_db SET SEARCH_PATH TO ${appfunc}_schema;

/* Set permissions for DDL, allowing usage and creating and data management
   operations in the schema. */
GRANT USAGE, CREATE ON SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_ddl;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_ddl;
GRANT EXECUTE ON ALL ROUTINES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_ddl;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN
    SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_ddl;

/* Grant default privileges to apply to future created objects. */
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO
    wf_${appname}_pg_app_ddl;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO
    wf_${appname}_pg_app_ddl;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl IN SCHEMA ${appfunc}_schema
    GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO
    wf_${appname}_pg_app_ddl;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO
    wf_${appname}_pg_app_ddl;

/* Set permissions for DML, allowing use of the schema, and data
   management operations in the schema. */
GRANT USAGE ON SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml;
GRANT EXECUTE ON ALL ROUTINES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN
    SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dml;

/* Grant default privileges to apply to future created objects. */
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO
    wf_${appname}_pg_app_dml;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO
    wf_${appname}_pg_app_dml;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl IN SCHEMA ${appfunc}_schema
    GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO
    wf_${appname}_pg_app_dml;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO
    wf_${appname}_pg_app_dml;

/* Set permissions for DQL, allowing use of the schema, and selecting
   from tables, both existing tables and tables created in the future. */
GRANT USAGE ON SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql;
GRANT EXECUTE ON ALL ROUTINES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql;
GRANT SELECT ON ALL TABLES IN SCHEMA ${appfunc}_schema TO
    wf_${appname}_pg_app_dql;

/* Grant default privileges to apply to future created objects. */
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT SELECT ON TABLES TO
    wf_${appname}_pg_app_dql;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO
    wf_${appname}_pg_app_dql;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl IN SCHEMA ${appfunc}_schema
    GRANT SELECT ON TABLES TO
    wf_${appname}_pg_app_dql;
ALTER DEFAULT PRIVILEGES
    FOR ROLE wf_${appname}_pg_app_ddl IN SCHEMA ${appfunc}_schema
    GRANT USAGE, SELECT ON SEQUENCES TO
        wf_${appname}_pg_app_dql;