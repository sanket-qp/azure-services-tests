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

    @pytest.mark.parametrize('user_tuple', [(common.get_app_ddl_user(), common.get_app_ddl_user())])
    def test_select(self, load_data):
        """
        Tests select query
        """
        ddl_user_connection, _ = load_data
        with ddl_user_connection.cursor() as cur:
            print ('SELECT * from %s' % common.get_article_table_name())
            cur.execute('SELECT * from %s' % common.get_article_table_name())
            x = cur.fetchall()
            print (x)
            assert 2 == len(x)
            assert 'hello_postgres' == x[0][1]
            assert 'hello_redis' == x[1][1]

    @pytest.mark.parametrize('user_tuple', [(common.get_app_ddl_user(), common.get_app_ddl_user())])
    def test_ddl_user_can_create_tables(self, load_data):
        """
        Tests access of app_ddl_user
        """
        ddl_user_connection, _ = load_data
        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__create_comments_table())
            print (x)

    def test_dql_user_cannot_create_tables(self, dql_user_connection):
        """
        Tests that dql_user shouldn't be able to create the tables
        """
        with pytest.raises(InsufficientPrivilege) as _:
            with dql_user_connection.cursor() as cur:
                ## cur.execute(self.__create_comments_table())
                common.execute_sql_file(dql_user_connection, "./sql/create_tables.sql")

    @pytest.mark.parametrize('user_tuple', [(common.get_app_ddl_user(), common.get_app_dql_user())])
    def test_dql_user_cannot_insert(self, load_data):
        ddl_user_connection, dql_user_connection = load_data


    @pytest.mark.parametrize('user_tuple', [(common.get_app_ddl_user(), common.get_app_dql_user())])
    def xtest_temp(self, load_data):
        dql_user_connection = load_data
        print (dql_user_connection)

    def __create_comments_table(self):
        return """
            CREATE TABLE %s.comments (
                id bigserial primary key,
                article_id bigserial NOT NULL,
                body varchar(128) NOT NULL,
                date_added timestamp default NOW()
            );
        """ % (common.get_schema_name())
