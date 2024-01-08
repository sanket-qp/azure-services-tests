# Replacing String with another string
def test_strReplace():
    string = "Hello, World!"
    assert string.replace("H", "J") == "Jello, World!"
# String Split - Splits a string to two substrings
def test_strSplit():
    string = "Hello,World"
    assert string.split(",") == ["Hello", "World"]
# String Strip
def test_strStrip():
    string = " Hello, World! "
    assert string.strip() == "Hello, World!"
# String Concatenate
def test_strConcat():
    string1 = "Hello"
    string2 = "World"
    assert string1 + string2 == "HelloWorld"

    # def get_admin_connection(self):
    #     return self.__get_connection(host='localhost', user='sanket', password='', port=5432, database='test_database')

    # def get_read_only_connection(self):
    #     return self.__get_connection(host='localhost', user='sanket', password='', port=5432, database='test_database')

    # @contextmanager
    # def __get_connection(self, host, port, database, user, password):
    #     try:
    #         print ("getting a connection")
    #         conn = psycopg2.connect(host=host, port=port, database=database, user=user)
    #         print ("got a connection")
    #         yield conn
    #     finally:
    #         print ("closing a connection")
    #         conn.close()
    #         print ("closed a connection")
        