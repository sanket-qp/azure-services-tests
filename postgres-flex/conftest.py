from string import Template

import common

import pytest


def pytest_addoption(parser):
    """
    Command line arguments specifying postgres connection parameters
    """
    parser.addoption("--host", action="store", default="localhost", help="postgres host")
    parser.addoption("--port", action="store", default=5432, help="postgres port")
    parser.addoption("--dbname", action="store", default="postgres", help="database name")
    parser.addoption("--admin_user", action="store", default="postgres",
                     help="postgres admin username")
    parser.addoption("--admin_password", action="store", default="",
                     help="postgres admin user's password")


@pytest.fixture(scope='module')
def connection_params(pytestconfig):
    """
    Fixture that returns postgres connection params
    """
    return {
        'host': pytestconfig.getoption("host"),
        'port': pytestconfig.getoption("port"),
        'database': pytestconfig.getoption("dbname"),
        'user': pytestconfig.getoption("admin_user"),
        'password': pytestconfig.getoption("admin_password")
    }

@pytest.fixture(scope='module')
def admin_connection(connection_params):
    """
    Fixture that returns postgres connection as an admin user
    """
    try:
        conn = common.get_db_connection(host=connection_params['host'],
                            port=connection_params['port'],
                            database=connection_params['database'],
                            user=connection_params['user'],
                            password=connection_params['password'])
        yield conn
    finally:
        conn.close()

@pytest.fixture(scope='module')
def ddl_user_connection(connection_params):
    """
    Fixture that returns postgres connection as a read_only user
    """
    print (connection_params)
    try:
        new_conn = common.get_db_connection(host=connection_params['host'],
                    port=connection_params['port'],
                    database=common.get_db_name(),
                    user=common.get_app_ddl_user(),
                    password=connection_params['password'])
        yield new_conn
    finally:
        new_conn.close()

@pytest.fixture(scope='module')
def dql_user_connection(connection_params):
    """
    Fixture that returns postgres connection as a read_only user
    """
    try:
        new_conn = None
        new_conn = common.get_db_connection(host=connection_params['host'],
                    port=connection_params['port'],
                    database=common.get_db_name(),
                    user=common.get_app_dql_user(),
                    password=connection_params['password'])
        yield new_conn
    finally:
        if new_conn:
            new_conn.close()

@pytest.fixture(scope='module')
def dml_user_connection(connection_params):
    """
    Fixture that returns postgres connection as a read_only user
    """
    try:
        new_conn = None
        new_conn = common.get_db_connection(host=connection_params['host'],
                    port=connection_params['port'],
                    database=common.get_db_name(),
                    user=common.get_app_dml_user(),
                    password=connection_params['password'])
        yield new_conn
    finally:
        if new_conn:
            new_conn.close()

@pytest.fixture(scope='module')
def ops_readwrite_connection(connection_params):
    """
    Fixture that returns postgres connection as a read_only user
    """
    try:
        new_conn = None
        new_conn = common.get_db_connection(host=connection_params['host'],
                    port=connection_params['port'],
                    database=common.get_db_name(),
                    user=common.get_ops_readwrite_user(),
                    password=connection_params['password'])
        yield new_conn
    finally:
        if new_conn:
            new_conn.close()

@pytest.fixture(scope='module')
def ops_readonly_connection(connection_params):
    """
    Fixture that returns postgres connection as a read_only user
    """
    try:
        new_conn = None
        new_conn = common.get_db_connection(host=connection_params['host'],
                    port=connection_params['port'],
                    database=common.get_db_name(),
                    user=common.get_ops_readonly_user(),
                    password=connection_params['password'])
        yield new_conn
    finally:
        if new_conn:
            new_conn.close()

@pytest.fixture(scope='module', autouse=True)
def create_database_and_connect(admin_connection, connection_params):
    """
    Fixture that creates an application database and connects to it
    """
    print (connection_params)
    # Create users and database
    execute_sql_file(admin_connection, "./sql/create_users_and_database.sql")
    
    # Connect to the created database
    try:
        new_conn = common.get_db_connection(host=connection_params['host'],
                            port=connection_params['port'],
                            database=common.get_db_name(),
                            user=connection_params['user'],
                            password=connection_params['password'])
        
        # Create permissions for the users
        execute_sql_file(new_conn, "./sql/grant_permissions.sql")
        yield new_conn
    finally:
        new_conn.close()

@pytest.fixture(scope='function', autouse=True)
def populate_data(connection_params, admin_connection):
    """
    A Fixture that runs before each test to set up database tables
    """
    try:
        conn = common.get_db_connection(host=connection_params['host'],
                        port=connection_params['port'],
                        database=common.get_db_name(),
                        user=connection_params['user'],
                        password=connection_params['password'])
        execute_sql_file(conn, "./sql/create_tables.sql")
        yield conn
        execute_sql_file(conn, "./sql/delete_tables.sql")
    finally:
        conn.close()

def execute_sql_file(connection, sql_file):
    """
    executes commands in the given sql file
    """
    with open(sql_file) as f:
        sql_template = f.read()
        sql = Template(sql_template).safe_substitute(
            {'appname': common.APP_NAME,
             'appfunc': common.APP_NAME,
             'admin_user': common.get_admin_user(),
             'password': common.get_password()})
        with connection.cursor() as cur:
            while len(sql):
                stmt, _, sql = sql.partition(';')
                if len(stmt.strip()):
                    # print (stmt.strip())
                    cur.execute(stmt.strip())
                    # print_grants(connection)         
                    
def print_grants(connection):
    with connection.cursor() as cur:
        stmt = """
        SELECT *
            FROM information_schema.role_table_grants 
            WHERE grantee like 'wf%';
        """
        print ("Printing Grants")
        cur.execute(stmt)
        for grant in cur.fetchall():
            print (grant)                    
