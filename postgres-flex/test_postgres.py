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

    def test_ddl_user_can_delete_tables(self, ddl_user_connection):
        """
        Tests access of app_ddl_user
        """
        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__delete_table_stmt())
            print (x)

    def test_dql_user_cannot_create_tables(self, dql_user_connection):
        """
        Tests that dql_user shouldn't be able to create the tables
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__create_comments_table())
        assert 'permission denied' in str(e)                

    def test_dql_user_can_select(self, dql_user_connection):
        """
        Tests that dql_user should be able to run select queries
        """
        with dql_user_connection.cursor() as cur:
            print ('SELECT * from %s' % common.get_article_table_name())
            cur.execute('SELECT * from %s' % common.get_article_table_name())
            x = cur.fetchall()
            print (x)
            assert 2 == len(x)

    def test_dql_user_cannot_insert(self, dql_user_connection):
        """
        Tests that verifies that dql_user shouldn't be able to insert data
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__insert_stmt())
        assert 'permission denied' in str(e)

    def test_dql_user_cannot_update(self, dql_user_connection):
        """
        Tests that verifies that dql_user shouldn't be able to insert data
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__update_stmt())
        assert 'permission denied' in str(e)
        

    def __create_comments_table(self):
        return """
            CREATE TABLE %s.comments (
                id bigserial primary key,
                article_id bigserial NOT NULL,
                body varchar(128) NOT NULL,
                date_added timestamp default NOW()
            );
        """ % (common.get_schema_name())

    def __insert_stmt(self):
        return """
            INSERT INTO %s.article (title, writeup) 
                VALUES
            ('hello_pytest', 'article about testing with pytest');
        """ % (common.get_schema_name())

    def __update_stmt(self):
        return """
            UPDATE %s.article
            SET writeup='testing with pytest is cool'
            WHERE title='hello_pytest';
        """ % (common.get_schema_name())

    def __delete_table_stmt(self):
        return """
            DROP TABLE %s.comments CASCADE
        """ % (common.get_schema_name())
       