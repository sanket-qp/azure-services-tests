from contextlib import contextmanager

import common

import pytest
import psycopg2
from psycopg2.errors import InsufficientPrivilege, UndefinedTable

class TestPostgresEngine:
    """
    A collection of tests to verify postgres engine functionality
    """

    def test_connection(self, db_connection):
        """
        Verifies an admin can connect to the database or not
        """
        assert db_connection is not None

    def test_connect_as_dml_user(self, dml_user_connection):
        """
        Verifies if a dml_user can connect to database or not
        """
        assert dml_user_connection is not None
        print (dml_user_connection)
        assert common.get_app_dml_user() == dml_user_connection.get_dsn_parameters().get('user')

        with dml_user_connection.cursor() as cur:
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            assert "15.5" in db_version[0]

    def test_connect_as_ddl_user(self, ddl_user_connection):
        """
        Verifies if a ddl_user can connect to database or not
        """
        assert ddl_user_connection is not None
        print (ddl_user_connection)
        assert common.get_app_ddl_user() == ddl_user_connection.get_dsn_parameters().get('user')

    def test_connect_as_dql_user(self, dql_user_connection):
        """
        Verifies if a dql_user can connect to database or not
        """
        assert dql_user_connection is not None
        print (dql_user_connection)
        assert common.get_app_dql_user() == dql_user_connection.get_dsn_parameters().get('user')

    def test_ddl_user_can_create_tables(self, ddl_user_connection):
        """
        Tests access of app_ddl_user
        """
        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__create_comments_table())
            print (x)

        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__delete_comments_table())
            print (x)

    def test_ddl_user_can_truncate_tables(self, ddl_user_connection):
        """
        Verifies that ddl_user can truncate the tables
        """
        # Make sure that data exists
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            x = cur.fetchall()
            #assert 2 == len(x)
            assert 'hello_postgres' == x[0][1]
            assert 'hello_redis' == x[1][1]  

        # Clear all the data
        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__truncate_table_stmt())
        
        # Verify that there are no rows in the table
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            x = cur.fetchall()
            assert 0 == len(x)
            
    def test_ddl_user_can_delete_tables(self, ddl_user_connection):
        """
        Verifies that ddl_user can delete the tables
        """
        with ddl_user_connection.cursor() as cur:
            cur.execute(self.__delete_article_table_stmt())

        # Query and make sure that table doesn't exist
        with pytest.raises(UndefinedTable) as e:
            with ddl_user_connection.cursor() as cur:
                cur.execute(f"SELECT * from {common.get_article_table_name()}")
        assert "does not exist" in str(e)

    def test_ddl_user_can_alter_tables(self, ddl_user_connection):
        """
        Verifies that ddl_user can alter the tables
        """
        # Alter the table
        with ddl_user_connection.cursor() as cur:
            x = cur.execute(self.__alter_table_stmt())
            
        # Verify that new column is added
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            x  = cur.fetchall()
            assert 2 == len(x)
            assert 'technology' == x[0][4]
            assert 'technology' == x[1][4]

    def test_dml_user_can_insert(self, dml_user_connection):
        """
        Verifies that dml_user can insert data in to tables
        """
        with dml_user_connection.cursor() as cur:
            x = cur.execute(self.__insert_stmt())
            print(x)
            cur.execute(self.__select_stmt())
            x = cur.fetchall()

    def test_dml_user_can_update(self, dml_user_connection):
        """
        Verifies that dml_user can insert data in to tables
        """
        with dml_user_connection.cursor() as cur:
            x = cur.execute(self.__update_stmt())
            print(x)
            cur.execute(self.__select_stmt())
            x = cur.fetchall()

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
            print (f'SELECT * from {common.get_article_table_name()}')
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
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
        return f"""
            CREATE TABLE {common.get_schema_name()}.comments (
                id bigserial primary key,
                article_id bigserial NOT NULL,
                body varchar(128) NOT NULL,
                date_added timestamp default NOW()
            );
        """

    def __delete_comments_table(self):
        return f"DROP TABLE {common.get_schema_name()}.comments"

    def __select_stmt(self):
        return f"SELECT * from {common.get_article_table_name()}"

    def __insert_stmt(self):
        return f"""
            INSERT INTO {common.get_article_table_name()} (title, writeup) 
                VALUES
            ('hello_pytest', 'article about testing with pytest');
        """

    def __update_stmt(self):
        return f"""
            UPDATE {common.get_article_table_name()}
            SET writeup='testing with pytest is cool'
            WHERE title='hello_pytest';
        """

    def __delete_article_table_stmt(self):
        return f"DROP TABLE {common.get_article_table_name()} CASCADE"
    
    def __truncate_table_stmt(self):
        return f"TRUNCATE TABLE {common.get_article_table_name()}"""
  
    def __alter_table_stmt(self):
        return f"""ALTER TABLE {common.get_article_table_name()} 
            ADD COLUMN category VARCHAR(20) DEFAULT 'technology'
            """
