/** Provisions roles, users, schema and database. For testing, run like:
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
* The remaining roles are operational, for read/write or just read access
* to system tables and parameters:
*
*    wf_${appname}_pg_ops_readwrite_role
*    wf_${appname}_pg_ops_readonly_role
*
* and application, for managing schemas, maintaining data, and only querying data:
*
*    wf_$${appname}_pg_app_ddl_role
*    wf_${appname}_pg_app_dml_role
*    wf_${appname}_pg_app_dql_role
*
* Naming conventions for databases, schema, and accounts:
*
*    Database: ${appname}_db
*    Schema: ${appfunc}
*    Accounts: wf_<${appname}>_pg_<ops|app>_<readonly|readwrite|ddl|dml|dql>_<role|user>
*
* Where:
*
*   - ${appname} is the name of the application that owns the database cluster.
*   - ${appfunc} is a functional name to give to the schema. Object names will
*     often by prepended by this schema name: ${appfunc}.tablename
*   - ops|app indicates either operations team or application team.
*   - readwrite|readonly|ddl|dml|dql indicates scope of the role or user:
*     > readwrite can read or update system tables and parameters on the cluster.
*     > readonly can only read system tables and parameters on the cluster.
*     > ddl can create, modify, and drop tables in an application database
*     create, modify, and drop tables
*     > dml cannot create, modify, or drop tables but can SELECT, INSERT,
*     UPDATE, DELETE, and TRUNCATE create, modify, and drop tables.
*     > dql can only SELECT from tables in the application database/schema
*  - role|user indicates if this is a group or individual user.
*
* The operational roles apply cluster wide and be assigned to either human
* users or tools run by human users.
*
* The application roles apply to databases in the cluster. Each application
* role will have a separate user in the default case. At some point, an
* application will need to combine the DDL and DML roles because their
* application maintains schema instead of using a separate dedicated tool.
*/
 

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
