from contextlib import contextmanager

import common

import pytest
import psycopg2
from psycopg2.errors import InsufficientPrivilege, UndefinedTable

@pytest.mark.engine
class TestPostgresEngine:
    """
    A collection of tests to verify postgres engine functionality
    """
    def test_connect_as_dml_user(self, dml_user_connection):
        """
        Verifies if a dml_user can connect to database or not
        """
        assert dml_user_connection is not None
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
        assert common.get_app_ddl_user() == ddl_user_connection.get_dsn_parameters().get('user')

    def test_connect_as_dql_user(self, dql_user_connection):
        """
        Verifies if a dql_user can connect to database or not
        """
        assert dql_user_connection is not None
        assert common.get_app_dql_user() == dql_user_connection.get_dsn_parameters().get('user')

    def test_ddl_user_can_create_tables(self, ddl_user_connection):
        """
        Tests access of app_ddl_user
        """
        with ddl_user_connection.cursor() as cur:
            cur.execute(self.__create_comments_table(common.get_schema_name()))

        with ddl_user_connection.cursor() as cur:
            cur.execute(self.__delete_comments_table())

    def test_ddl_user_can_truncate_tables(self, ddl_user_connection):
        """
        Verifies that ddl_user can truncate the tables
        """
        # Make sure that data exists
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]

        # Clear all the data
        with ddl_user_connection.cursor() as cur:
            cur.execute(self.__truncate_table_stmt())
        
        # Verify that there are no rows in the table
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 0 == len(rs)
            
    def test_ddl_user_can_delete_tables(self, ddl_user_connection):
        """
        Verifies that ddl_user can delete the tables
        """
        # Delete the table
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
            cur.execute(self.__alter_table_stmt())
            
        # Verify that new column is added
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs  = cur.fetchall()
            assert 2 == len(rs)
            assert 'technology' == rs[0][4]
            assert 'technology' == rs[1][4]

    @pytest.mark.negative
    def test_ddl_user_cannot_create_table_in_public_schema(self, ddl_user_connection):
        """
        Tests access of app_ddl_user
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with ddl_user_connection.cursor() as cur:
                cur.execute(self.__create_comments_table("public"))
        assert "permission denied for schema public" in str(e)

    def test_dml_user_can_insert(self, dml_user_connection):
        """
        Verifies that dml_user can insert data in to tables
        """
        with dml_user_connection.cursor() as cur:
            cur.execute(self.__insert_stmt())
            cur.execute(self.__select_stmt())
            rs = cur.fetchall()
            assert 3 == len(rs)
            assert 'hello_pytest' == rs[-1][1]

    def test_dml_user_can_update(self, dml_user_connection):
        """
        Verifies that dml_user can insert data in to tables
        """
        with dml_user_connection.cursor() as cur:
            cur.execute(self.__update_stmt())
            cur.execute(self.__select_stmt())
            rs = cur.fetchall()
            assert 'redis is cool' == rs[-1][2]

    @pytest.mark.negative
    def test_dml_user_cannot_create_table(self, dml_user_connection):
        """
        Tests access of app_ddl_user
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dml_user_connection.cursor() as cur:
                cur.execute(self.__create_comments_table(common.get_schema_name()))
        assert "permission denied" in str(e)

    @pytest.mark.negative
    def test_dml_user_cannot_delete_table(self, dml_user_connection):
        """
        Tests access of app_ddl_user
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dml_user_connection.cursor() as cur:
                cur.execute(self.__delete_article_table_stmt())
        assert "must be owner of table" in str(e)

    @pytest.mark.negative
    def test_dql_user_cannot_create_tables(self, dql_user_connection):
        """
        Tests that dql_user shouldn't be able to create the tables
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__create_comments_table(common.get_schema_name()))
        assert 'permission denied' in str(e)  

    def test_dql_user_can_select(self, dql_user_connection):
        """
        Tests that dql_user should be able to run select queries
        """
        with dql_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            x = cur.fetchall()
            assert 2 == len(x)

    @pytest.mark.negative
    def test_dql_user_cannot_insert(self, dql_user_connection):
        """
        Tests that verifies that dql_user shouldn't be able to insert data
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__insert_stmt())
        assert 'permission denied' in str(e)

    @pytest.mark.negative
    def test_dql_user_cannot_update(self, dql_user_connection):
        """
        Tests that verifies that dql_user shouldn't be able to insert data
        """
        with pytest.raises(InsufficientPrivilege) as e:
            with dql_user_connection.cursor() as cur:
                cur.execute(self.__update_stmt())
        assert 'permission denied' in str(e)    

    def __create_comments_table(self, schema_name):
        return f"""
            CREATE TABLE {schema_name}.comments (
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
            SET writeup='redis is cool'
            WHERE title='hello_redis';
        """

    def __delete_article_table_stmt(self):
        return f"DROP TABLE {common.get_article_table_name()} CASCADE"
    
    def __truncate_table_stmt(self):
        return f"TRUNCATE TABLE {common.get_article_table_name()}"""
  
    def __alter_table_stmt(self):
        return f"""ALTER TABLE {common.get_article_table_name()} 
            ADD COLUMN category VARCHAR(20) DEFAULT 'technology'
            """