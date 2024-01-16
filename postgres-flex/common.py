import psycopg2

APP_NAME = "mysimpleblog"

def get_schema_name():
    return f"{APP_NAME}_schema"

def get_db_name():
    return f"{APP_NAME}_db"

def get_article_table_name():
    return f"{get_schema_name()}.article"

def get_password():
    return "s3cr3t!"

def get_ops_readwrite_user():
    return f"wf_{APP_NAME}_pg_ops_readwrite"

def get_ops_readwrite_tool_user():
    return f"wf_{APP_NAME}_pg_ops_readwrite_tool_user"

def get_ops_readwrite_role():
    return f"wf_{APP_NAME}_pg_ops_readwrite_role"

def get_ops_readonly_user():
    return f"wf_{APP_NAME}_pg_ops_readonly_user"

def get_ops_readonly_tool_user():
    return f"wf_{APP_NAME}_pg_ops_readonly_tool_user"

def get_ops_readonly_role():
    return f"wf_{APP_NAME}_pg_ops_readonly_role"

def get_app_ddl_user():
    return f"wf_{APP_NAME}_pg_app_ddl"

def get_app_ddl_role():
    return f"wf_{APP_NAME}_pg_app_ddl_role"

def get_app_dml_user():
    return f"wf_{APP_NAME}_pg_app_dml"

def get_app_dml_role():
    return f"wf_{APP_NAME}_pg_app_dml_role"

def get_app_dql_user():
    return f"wf_{APP_NAME}_pg_app_dql"

def get_app_dql_role():
    return f"wf_{APP_NAME}_pg_app_dql_role"

def get_db_connection(host, port, database, user, password):
    """
    Returns a postgres connection object for given parameters
    """
    conn = psycopg2.connect(host=host,
                            port=port,
                            database=database,
                            user=user,
                            password=password)
    conn.set_session(autocommit=True)
    return conn

def get_db_connection_as_user(host, port, get_database_func, get_user_func, password):
    return get_db_connection(host, port, get_database_func(), get_user_func(), password)
