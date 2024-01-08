import pytest
import psycopg2

@pytest.fixture(scope='module')
def connection_params():
    return {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_database',
        'user': 'sanket',
        'password': ''
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
