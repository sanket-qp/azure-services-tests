from contextlib import contextmanager

import psycopg2

class TestPostgres:
    def test_connection(self, load_data):
        print ("testing connection")
        admin_connection = load_data
        with admin_connection.cursor() as cur:
            cur = admin_connection.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            assert "15.5" in db_version[0]
        
    def test_query(self, admin_connection):
        print ("testing query")
        with admin_connection.cursor() as cur:
            cur.execute('SELECT * from test_schema.article')
            x = cur.fetchall()
            assert 2 == len(x)
            assert 'hello_postgres' == x[0][1]            
            assert 'hello_redis' == x[1][1]
            