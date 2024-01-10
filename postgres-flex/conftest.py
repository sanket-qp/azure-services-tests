from string import Template
import config

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

@pytest.fixture(scope='module')
def admin_connection(connection_params):
    """
    Fixture that returns postgres connection as an admin user
    """
    try:
        conn = psycopg2.connect(host=connection_params['host'],
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
def load_data(admin_connection):
    """
    Fixture that loads the data using admin connection
    """
    try:
        prepare_database(admin_connection)
        yield admin_connection
    finally:
        clear_database(admin_connection)


def prepare_database(connection):
    """
    Prepares a postgres schema by executing the `load_data.sql` file
    """
    print ("loading data")
    clear_database(connection)
    execute_sql_file(connection, "create_database.sql")
    execute_sql_file(connection, "create_user_roles.sql")
    execute_sql_file(connection, "create_permissions.sql")
    execute_sql_file(connection, "create_tables.sql")

def clear_database(connection):
    """
    Clears postgres database by executing the `clear_data.sql` file
    """
    print ("clearing data")
    execute_sql_file(connection, "delete_permissions.sql")
    execute_sql_file(connection, "delete_database.sql")
    execute_sql_file(connection, "delete_user_roles.sql")
    ## execute_sql_file(connection, "clear_data.sql")

def execute_sql_file(connection, sql_file):
    """
    executes commands in the given sql file
    """
    with open(sql_file) as f:
        sql_template = f.read()
        sql = Template(sql_template).safe_substitute(
            {'appname': config.APP_NAME, 'appfunc': config.APP_NAME})
        with connection.cursor() as cur:
            cur.execute(sql)
                                