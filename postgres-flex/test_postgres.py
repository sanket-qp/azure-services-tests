from contextlib import contextmanager

import common

import pytest
import psycopg2
from psycopg2.errors import InsufficientPrivilege

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

    def test_ddl_user_can_create_tables(self, ddl_user_connection):
        """
        Tests access of app_ddl_user
        """
        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__create_comments_table())
            print (x)

    def test_dql_user_cannot_create_tables(self, dql_user_connection):
        """
        Tests that dql_user shouldn't be able to create the tables
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__create_comments_table())

    def __create_comments_table(self):
        return """
            CREATE TABLE %s.comments (
                id bigserial primary key,
                article_id bigserial NOT NULL,
                body varchar(128) NOT NULL,
                date_added timestamp default NOW()
            );
        """ % (common.get_schema_name())
