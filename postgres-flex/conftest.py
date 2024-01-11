from string import Template

import common

import pytest

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
        new_conn = common.get_db_connection(host=connection_params['host'],
                    port=connection_params['port'],
                    database=common.get_db_name(),
                    user=common.get_app_dql_user(),
                    password=connection_params['password'])
        yield new_conn
    finally:
        new_conn.close()


@pytest.fixture(scope='module')
def create_database_and_connect(admin_connection, connection_params):
    """
    Fixture that creates an application database and connects to it using admin user
    """
    clear_database(admin_connection)
    common.execute_sql_file(admin_connection, "./sql/create_database.sql")
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
def db_connection(create_database_and_connect):
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


@pytest.fixture(scope='function')
def load_data(connection_params, user_tuple):
    """
    A Fixture that runs before each test and loads the data using the user `load_us_user`
    and returns a database connection using `connect_as_user`

    :param user_tuple: a tuple of user names, 
                first element specifies the user to load the data
                second element specifies the user to connect as after data is loaded
    """
    try:
        print ("HELLO:", user_tuple)
        print ("connection params:", connection_params)
        load_as_user = user_tuple[0]
        connect_as_user = user_tuple[1]
        load_as_connection = connect_as_connection = None
        load_as_connection = common.get_db_connection(host=connection_params['host'],
                                port=connection_params['port'],
                                database=common.get_db_name(),
                                user=load_as_user,
                                password=connection_params['password'])

        common.execute_sql_file(load_as_connection, "./sql/create_tables.sql")
        connect_as_connection = common.get_db_connection(host=connection_params['host'],
                                port=connection_params['port'],
                                database=common.get_db_name(),
                                user=connect_as_user,
                                password=connection_params['password'])

        yield load_as_connection, connect_as_connection
    finally:
        common.execute_sql_file(load_as_connection, "./sql/delete_tables.sql")
        if load_as_connection:
            load_as_connection.close()
        if connect_as_connection:
            connect_as_connection.close()


def prepare_database(connection):
    """
    Prepares a postgres schema by executing the sql files
    """
    common.execute_sql_file(connection, "./sql/create_user_roles.sql")
    common.execute_sql_file(connection, "./sql/create_permissions.sql")
    ## execute_sql_file(connection, "./sql/create_tables.sql")

def clear_database(connection):
    """
    Clears postgres database by executing the `clear_data.sql` file
    """
    print ("clearing data")
    common.execute_sql_file(connection, "./sql/delete_permissions.sql")
    common.execute_sql_file(connection, "./sql/delete_database.sql")
    common.execute_sql_file(connection, "./sql/delete_user_roles.sql")
    common.execute_sql_file(connection, "./sql/delete_tables.sql")
