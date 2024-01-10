from contextlib import contextmanager
import config

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
            admin_connection.commit()
    
    def test_select(self, admin_connection):
        print ("testing query")
        with admin_connection.cursor() as cur:
            cur.execute('SELECT * from %s' % config.get_article_table_name())
            x = cur.fetchall()
            assert 2 == len(x)
            assert 'hello_postgres' == x[0][1]
            assert 'hello_redis' == x[1][1]
            admin_connection.commit()
