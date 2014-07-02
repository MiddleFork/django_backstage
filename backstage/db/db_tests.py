__author__ = 'walker'
import unittest
import psycopg2

class TestDatabaseFunctionality(unittest.TestCase):

    def setUp(self):
        pass


    def test_connect(self):
        """ Test that we can connect to the database server
        @return:
        """
        conn = psycopg2.connect("dbname=backstage host=127.0.0.1 user=backstage")


    def test_create(self):
        """
        Test that we can create a database within the db server
        @return:
        """


if __name__ == '__main__':
    unittest.main()