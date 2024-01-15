from string import Template

import common

import pytest

import sys

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
        print ("got an admin connection")
        yield conn
    finally:
        conn.close()
        print ("closing an admin connection")

@pytest.fixture(scope='module')
def ddl_user_connection(connection_params):
    """
    Fixture that returns postgres connection as a read_only user
    """
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
def xcreate_database_and_connect(admin_connection, connection_params):
    """
    Fixture that creates an application database and connects to it
    """
    clear_database(admin_connection)
    execute_sql_file(admin_connection, "./sql/create_database.sql")
    new_db = common.get_db_name()
    try:
        new_conn = common.get_db_connection(host=connection_params['host'],
                            port=connection_params['port'],
                            database=new_db,
                            user=connection_params['user'],
                            password=connection_params['password'])
        yield new_conn
    finally:
        print ("Closing new_conn")
        new_conn.close()

@pytest.fixture(scope='module')
def create_database_and_connect(admin_connection, connection_params):
    """
    Fixture that creates an application database and connects to it
    """
    execute_sql_file(admin_connection, "./sql/script1.sql")
    new_db = common.get_db_name()
    try:
        new_conn = common.get_db_connection(host=connection_params['host'],
                            port=connection_params['port'],
                            database=new_db,
                            user=connection_params['user'],
                            password=connection_params['password'])
        
        execute_sql_file(new_conn, "./sql/script2.sql")
        yield new_conn
    finally:
        print ("Closing new_conn")
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
                        user=common.get_app_ddl_user(),
                        ## user=connection_params['user'],
                        password=connection_params['password'])
        execute_sql_file(conn, "./sql/create_tables.sql")
        yield conn
        execute_sql_file(conn, "./sql/delete_tables.sql")
    finally:
        conn.close()

@pytest.fixture(scope='module')
def xdb_connection(create_database_and_connect):
    """
    Fixture that loads the data in to sample application database and returns the connection 
    """
    try:
        connection = create_database_and_connect
        prepare_database(connection)
        yield connection
    finally:
        ## clear_database(admin_connection)
        print ("Clearning data")

@pytest.fixture(scope='module')
def db_connection(create_database_and_connect, admin_connection):
    """
    Fixture that loads the data in to sample application database and returns the connection 
    """
    try:
        ## clear_database(admin_connection)
        ## execute_sql_file(admin_connection, "./sql/script1.sql")
        connection = create_database_and_connect
        ## execute_sql_file(admin_connection, "./sql/script2.sql")
        yield connection
    finally:
        ## clear_database(admin_connection)
        print ("Clearning data")

def prepare_database(connection):
    """
    Prepares a postgres schema by executing the sql files
    """
    execute_sql_file(connection, "./sql/create_user_roles.sql")
    execute_sql_file(connection, "./sql/create_permissions.sql")

def clear_database(connection):
    """
    Clears postgres database by executing the `clear_data.sql` file
    """
    print ("clearing data")
    execute_sql_file(connection, "./sql/delete_permissions.sql")
    execute_sql_file(connection, "./sql/delete_database.sql")
    execute_sql_file(connection, "./sql/delete_user_roles.sql")

def execute_sql_file(connection, sql_file):
    """
    executes commands in the given sql file
    """
    print ("---------------------------------------------------------")
    print (f"executing: {sql_file}")
    with open(sql_file) as f:
        sql_template = f.read()
        sql = Template(sql_template).safe_substitute(
            {'appname': common.APP_NAME, 'appfunc': common.APP_NAME})
        with connection.cursor() as cur:
            ## print (sql)
            print ("--------")
            while len(sql):
                stmt, _, sql = sql.partition(';')
                if "wf_mysimpleblog_pg_app_dql_role" in stmt.strip():
                    print ("Check HERE")
                if len(stmt.strip()):
                    print ("HELLO", stmt.strip()) 
                    rtn = cur.execute(stmt.strip())
                    print ("return: %s" % rtn)
                    print_grants(connection)
                    print ("====")            
            ## rtn = cur.execute(sql)
    print ("---------------------------------------------------------")
                    
def print_grants(connection):
    with connection.cursor() as cur:
        stmt = """
        SELECT *
            FROM information_schema.role_table_grants 
            WHERE grantee like 'wf%';
        """
        print ("Printing Grants")
        x = cur.execute(stmt)
        rtn = cur.fetchall()
        for grant in rtn:
            print (grant)        
