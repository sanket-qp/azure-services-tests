import pytest
import psycopg2

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="localhost", help="postgres host")
    parser.addoption("--port", action="store", default=5432, help="postgres port")
    parser.addoption("--dbname", action="store", default="test_database", help="database name")
    parser.addoption("--admin_user", action="store", default="sanket", help="postgres admin username")
    parser.addoption("--admin_password", action="store", default="", help="postgres admin user's password")


@pytest.fixture(scope='module')
def connection_params(pytestconfig):
    return {
        'host': pytestconfig.getoption("host"),
        'port': pytestconfig.getoption("port"),
        'database': pytestconfig.getoption("dbname"),
        'user': pytestconfig.getoption("admin_user"),
        'password': pytestconfig.getoption("admin_password")
    }

@pytest.fixture(scope='module')
def admin_connection(connection_params):
    conn = psycopg2.connect(host=connection_params['host'], 
                            port=connection_params['port'], 
                            database=connection_params['database'], 
                            user=connection_params['user'],
                            password=connection_params['password'])
    print ("got an admin connection")
    conn.set_session(autocommit=True)
    yield conn
    conn.close()
    print ("closing an admin connection")

@pytest.fixture(scope='module')
def readonly_connection():
    print ("entering readonly_connection")
    yield
    print ("exiting readonly_connections")

@pytest.fixture(scope='module')
def load_data(admin_connection):    
    prepare_schema(admin_connection)
    yield admin_connection
    delete_schema(admin_connection)

def prepare_schema(connection):
    print ("loading data")
    with connection.cursor() as cur:
        cur.execute(open("load_data.sql", "r").read())

def delete_schema(connection):
    print ("clearing data")
    with connection.cursor() as cur:
        cur.execute(open("clear_data.sql", "r").read())
