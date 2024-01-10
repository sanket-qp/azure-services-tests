from string import Template
import config
import sys

import pytest
import psycopg2

def pytest_addoption(parser):
    """
    Command line arguments specifying postgres connection parameters
    """
    parser.addoption("--host", action="store", default="localhost", help="postgres host")
    parser.addoption("--port", action="store", default=5432, help="postgres port")
    parser.addoption("--dbname", action="store", default="test_database", help="database name")
    parser.addoption("--admin_user", action="store", default="sanket",
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

def connect_to_db(host, port, database, user, password):
    return psycopg2.connect(host=host,
                            port=port,
                            database=database,
                            user=user,
                            password=password)

@pytest.fixture(scope='module')
def admin_connection(connection_params):
    """
    Fixture that returns postgres connection as an admin user
    """
    try:
        conn = connect_to_db(host=connection_params['host'],
                            port=connection_params['port'],
                            database=connection_params['database'],
                            user=connection_params['user'],
                            password=connection_params['password'])
        print ("got an admin connection")
        conn.set_session(autocommit=True)
        yield conn
    finally:
        conn.close()
        print ("closing an admin connection")

@pytest.fixture(scope='module')
def readonly_connection():
    """
    Fixture that returns postgres connection as a read_only user
    """
    print ("entering readonly_connection")
    yield
    print ("exiting readonly_connections")

@pytest.fixture(scope='module')
def load_data(create_database_and_connect):
    """
    Fixture that loads the data using admin connection
    """
    try:
        connection = create_database_and_connect
        prepare_database(connection)
        yield connection
    finally:
        ## clear_database(admin_connection)
        pass

@pytest.fixture(scope='module')
def create_database_and_connect(admin_connection, connection_params):
    """
    Fixture that creates an application database and connects to it
    """
    clear_database(admin_connection)
    execute_sql_file(admin_connection, "./sql/create_database.sql")
    new_db = config.get_db_name()
    try:
        new_conn = connect_to_db(host=connection_params['host'],
                            port=connection_params['port'],
                            database=new_db,
                            user=connection_params['user'],
                            password=connection_params['password'])
        yield new_conn
    finally:
        new_conn.close()

def prepare_database(connection):
    """
    Prepares a postgres schema by executing the `load_data.sql` file
    """
    print ("loading data")
    # execute_sql_file(connection, "./sql/create_database.sql")
    execute_sql_file(connection, "./sql/create_user_roles.sql")
    execute_sql_file(connection, "./sql/create_permissions.sql")
    execute_sql_file(connection, "./sql/create_tables.sql")

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
    print ("executing: %s" % sql_file)
    with open(sql_file) as f:
        sql_template = f.read()
        sql = Template(sql_template).safe_substitute(
            {'appname': config.APP_NAME, 'appfunc': config.APP_NAME})
        with connection.cursor() as cur:
            #print (sql)
            #print ("--------")
            rtn = cur.execute(sql)
            #print ("return: %s" % rtn)
    print ("---------------------------------------------------------")                                