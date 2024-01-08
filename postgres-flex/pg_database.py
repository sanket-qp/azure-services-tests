import logging
from contextlib import contextmanager

import psycopg2.pool as pool

# Connetion pool will start the pool
# Close the pool 

# Database will get the connection from pool
# execute the query 
# release the connection

class ConnectionPool:
    def __init__(self):
        pass

    def __enter__(self):
        print ("getting a connection")

    def __exit__(self):
        print ("releasing a connection")

    @contextmanager
    def get(self):
        pass

    def close_all(self):
        pass

class Database:
    def __init__(self, pool):
        self.pool = pool

    def query(self):
        with self.pool.get_connection() as conn:
            print ("Query")

    def select(self):
        print ("Select")

class Test:
    def setUp(self):
        self.pool = ConnectionPool()

    def testInsert(self):
        with self.pool.get() as conn:
            with Database(conn) as db:
                db.query()

    def testSelect(self):
        with self.pool.get() as conn:
            with Database(conn) as db:
                db.select()

    def tearDown(self):
        self.pool.close_all()

def main():
    test = Test()
    test.setUp()
    test.testInsert()
    test.testSelect()
    test.tearDown()

if __name__ == "__main__":
    main()

