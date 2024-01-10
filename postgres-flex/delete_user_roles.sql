
/* Make sure operation users do not exist. */
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
 SELECT 1;
