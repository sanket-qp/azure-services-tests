from contextlib import contextmanager
import common

import psycopg2

class TestPostgres:
    def test_connection(self, db_connection):
        """
        Tests database connection
        """
        print ("testing connection")
        with db_connection.cursor() as cur:
            cur = db_connection.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print ("db version: %s" % db_version)
            assert "15.5" in db_version[0]

    def test_select(self, db_connection):
        """
        Tests select query
        """
        with db_connection.cursor() as cur:
            print ('SELECT * from %s' % common.get_article_table_name());
            cur.execute('SELECT * from %s' % common.get_article_table_name())
            x = cur.fetchall()
            print (x)
            assert 2 == len(x)
            assert 'hello_postgres' == x[0][1]
            assert 'hello_redis' == x[1][1]
