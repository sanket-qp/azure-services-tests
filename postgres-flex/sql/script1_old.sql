DROP SCHEMA IF EXISTS ${appfunc}_schema CASCADE;

DROP DATABASE IF EXISTS ${appname}_db;

DROP USER IF EXISTS wf_${appname}_pg_ops_readonly_user;
DROP USER IF EXISTS wf_${appname}_pg_ops_readwrite_user;
DROP USER IF EXISTS wf_${appname}_pg_ops_readonly_tool_user;
DROP USER IF EXISTS wf_${appname}_pg_ops_readwrite_tool_user;
 
/* Make sure application users do not exist. */
DROP USER IF EXISTS wf_${appname}_pg_app_ddl_user;
DROP USER IF EXISTS wf_${appname}_pg_app_dml_user;
DROP USER IF EXISTS wf_${appname}_pg_app_dql_user;
 
/* Make sure operations roles do not exist. */
DROP ROLE IF EXISTS wf_${appname}_pg_ops_readonly_role;
DROP ROLE IF EXISTS wf_${appname}_pg_ops_readwrite_role;
 
/* Make sure application roles do not exist. */
DROP ROLE IF EXISTS wf_${appname}_pg_app_ddl_role;
DROP ROLE IF EXISTS wf_${appname}_pg_app_dml_role;
DROP ROLE IF EXISTS wf_${appname}_pg_app_dql_role;

/* Create operational roles, explicitly turning off attributes, and
   limiting connections. */
CREATE ROLE wf_${appname}_pg_ops_readonly_role WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOLOGIN
    NOREPLICATION
    NOBYPASSRLS
    CONNECTION LIMIT 2;
CREATE ROLE wf_${appname}_pg_ops_readwrite_role WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOLOGIN
    NOREPLICATION
    NOBYPASSRLS
    CONNECTION LIMIT 2;
 
/* Grant permissions to the operational roles. */
GRANT pg_read_all_settings TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_read_all_stats TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_stat_scan_tables TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_read_all_data TO wf_${appname}_pg_ops_readonly_role;
 
GRANT pg_read_all_settings TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_read_all_stats TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_stat_scan_tables TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_read_all_data TO wf_${appname}_pg_ops_readonly_role;
GRANT pg_write_all_data TO wf_${appname}_pg_ops_readwrite_role;
 
/* Create operational users, for both human users and automated tools. */
CREATE USER wf_${appname}_pg_ops_readwrite_user WITH ROLE wf_${appname}_pg_ops_readwrite_role;
CREATE USER wf_${appname}_pg_ops_readonly_user WITH ROLE wf_${appname}_pg_ops_readonly_role;
CREATE USER wf_${appname}_pg_ops_readwrite_tool_user WITH ROLE wf_${appname}_pg_ops_readwrite_role;
CREATE USER wf_${appname}_pg_ops_readonly_tool_user WITH ROLE wf_${appname}_pg_ops_readonly_role;
 
/* Create application roles, explicitly turning off attributes. */
CREATE ROLE wf_${appname}_pg_app_ddl_role WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOLOGIN
    NOREPLICATION
    NOBYPASSRLS;
CREATE ROLE wf_${appname}_pg_app_dml_role WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOLOGIN
    NOREPLICATION
    NOBYPASSRLS;
CREATE ROLE wf_${appname}_pg_app_dql_role WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOLOGIN
    NOREPLICATION
    NOBYPASSRLS;
 
/* Create application users for programmatic use. */
CREATE USER wf_${appname}_pg_app_ddl_user;
CREATE USER wf_${appname}_pg_app_dml_user;
CREATE USER wf_${appname}_pg_app_dql_user;
 
/* Assign roles to application users. */
GRANT wf_${appname}_pg_app_ddl_role TO wf_${appname}_pg_app_ddl_user;
GRANT wf_${appname}_pg_app_dml_role TO wf_${appname}_pg_app_dml_user;
GRANT wf_${appname}_pg_app_dql_role TO wf_${appname}_pg_app_dql_user;

CREATE DATABASE ${appname}_db;
