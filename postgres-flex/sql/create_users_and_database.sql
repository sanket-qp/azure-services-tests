/*
 * Provisions roles, users, schema and database. For testing, run like:
 *
 *    psql -U admin -f sql/provision.sql
 *
 * If testing in a local database then admin is the user it was installed
 * under.
 *
 * The top most account for PG Flex is azure_pg_admin. This account is used by
 * Azure for other tasks. Thus wf_${appname}_pg_admin is used to run these scripts
 * as the top-most account. It will have the same privileges as azure_pg_admin
 * and be created before this script is run.
 *
 * The remaining users are operational, for read/write or just read access
 * to system tables and parameters:
 *
 *    wf_${appname}_pg_readwrite
 *    wf_${appname}_pg_readonly
 *
 * and application, for managing schemas, maintaining data, and only querying data:
 *
 *    wf_${appname}_pg_app_ddl
 *    wf_${appname}_pg_app_dml
 *    wf_${appname}_pg_app_dql
 *
 * Naming conventions for databases, schema, and accounts:
 *
 *    Database: ${appname}_db
 *    Schema: appfunc
 *    Accounts: wf_<appname>_pg_<ops|app>_<readonly|readwrite|ddl|dml|dql>
 *
 * Where:
 *
 *   - appname is the name of the application that owns the database cluster.
 *   - appfunc is a functional name to give to the schema. Object names will
 *     often by prepended by this schema name: appfunc.tablename
 *   - ops|app indicates either operations team or application team.
 *   - readwrite|readonly|ddl|dml|dql indicates scope of the role or user:
 *     > readwrite can read or update system tables and parameters on the cluster.
 *     > readonly can only read system tables and parameters on the cluster.
 *     > ddl can create, modify, and drop tables in an application database
 *     create, modify, and drop tables
 *     > dml cannot create, modify, or drop tables but can SELECT, INSERT,
 *     UPDATE, DELETE, and TRUNCATE create, modify, and drop tables.
 *     > dql can only SELECT from tables in the application database/schema
 *
 * The operational roles apply cluster wide and be assigned to either human
 * users or tools run by human users.
 *
 * The application users apply to databases in the cluster. The users are
 * additive in the sense that DML can do everything DQL does plus write to
 * tables, DDL can do everything DML does plus create and modify table schema.
 */

/* Make sure database and schema does not exist. */
DROP SCHEMA IF EXISTS ${appfunc}_schema;
DROP DATABASE IF EXISTS ${appfunc}_db;

/* Make sure operation users do not exist. */
DROP USER IF EXISTS wf_${appname}_pg_ops_readonly;
DROP USER IF EXISTS wf_${appname}_pg_ops_readwrite;

/* Make sure application users do not exist. */
DROP USER IF EXISTS wf_${appname}_pg_app_ddl;
DROP USER IF EXISTS wf_${appname}_pg_app_dml;
DROP USER IF EXISTS wf_${appname}_pg_app_dql;

/* Create operational roles, explicitly turning off attributes, and
   limiting connections. */
CREATE USER wf_${appname}_pg_ops_readonly WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    LOGIN
    NOREPLICATION
    NOBYPASSRLS
    CONNECTION LIMIT 2;
CREATE USER wf_${appname}_pg_ops_readwrite WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    LOGIN
    NOREPLICATION
    NOBYPASSRLS
    CONNECTION LIMIT 2;

/* Grant permissions to the operational roles. */
GRANT pg_read_all_settings TO wf_${appname}_pg_ops_readonly;
GRANT pg_read_all_stats TO wf_${appname}_pg_ops_readonly;
GRANT pg_stat_scan_tables TO wf_${appname}_pg_ops_readonly;
GRANT pg_read_all_data TO wf_${appname}_pg_ops_readonly;

GRANT pg_read_all_settings TO wf_${appname}_pg_ops_readwrite;
GRANT pg_read_all_stats TO wf_${appname}_pg_ops_readwrite;
GRANT pg_stat_scan_tables TO wf_${appname}_pg_ops_readwrite;
GRANT pg_read_all_data TO wf_${appname}_pg_ops_readwrite;
GRANT pg_write_all_data TO wf_${appname}_pg_ops_readwrite;

/* Create application users. */
CREATE ROLE wf_${appname}_pg_app_ddl WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    LOGIN
    NOREPLICATION
    NOBYPASSRLS;
CREATE ROLE wf_${appname}_pg_app_dml WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    LOGIN
    NOREPLICATION
    NOBYPASSRLS;
CREATE ROLE wf_${appname}_pg_app_dql WITH
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    LOGIN
    NOREPLICATION
    NOBYPASSRLS;

CREATE DATABASE ${appfunc}_db;