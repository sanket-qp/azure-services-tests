APP_NAME = "mysimpleblog"

def get_schema_name():
    return "%s_schema" % APP_NAME

def get_db_name():
    return "%s_db" % APP_NAME

def get_article_table_name():
    return "%s.article" % get_schema_name()

def get_password():
    return "s3cr3t!"

def get_ops_readwrite_user():
    return "wf_%s_pg_ops_readwrite_user" % (APP_NAME)

def get_ops_readwrite_tool_user():
    return "wf_%s_pg_ops_readwrite_tool_user" % (APP_NAME)

def get_ops_readwrite_role():
    return "wf_%s_pg_ops_readwrite_role" % (APP_NAME)

def get_ops_readonly_user():
    return "wf_%s_pg_ops_readonly_user" % (APP_NAME)

def get_ops_readonly_tool_user():
    return "wf_%s_pg_ops_readonly_tool_user" % (APP_NAME)

def get_ops_readonly_role():
    return "wf_%s_pg_ops_readonly_role" % (APP_NAME)

def get_app_ddl_user():
    return "wf_%s_pg_app_ddl_user" % (APP_NAME)

def get_app_ddl_role():
    return "wf_%s_pg_app_ddl_role" % (APP_NAME)

def get_app_dml_user():
    return "wf_%s_pg_app_dml_user" % (APP_NAME)

def get_app_dml_role():
    return "wf_%s_pg_app_dml_role" % (APP_NAME)

def get_app_dql_user():
    return "wf_%s_pg_app_dql_user" % (APP_NAME)

def get_app_dql_role():
    return "wf_%s_pg_app_dql_role" % (APP_NAME)
