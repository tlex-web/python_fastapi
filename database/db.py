import mysql.connector
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
import configparser
import time

config = configparser.ConfigParser()
config.read('./config.ini')


class Database():

    def __init__(self) -> None:
        self.host = config['DEVELOPMENT']['Host']
        self.port = config['DEVELOPMENT'].getint('Port')
        self.user = config['DEVELOPMENT']['User']
        self.password = config['DEVELOPMENT']['Password']
        self.database = config['DEVELOPMENT']['Database']
        self.cnx = None

    def connect(self) -> MySQLConnection | PooledMySQLConnection:

        config = {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'raise_on_warnings': True
        }

        while True:
            try:
                self.cnx = mysql.connector.connect(**config)

                return self.cnx

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print('wrong username or password')
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print('database does not exist')
                else:
                    print(f"Error: {err}")
                time.sleep(5)

    def get_posts(self) -> list:

        cnx = self.connect()
        cursor = cnx.cursor()

        query = "SELECT * FROM tblposts"
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        cnx.close()

        return rows

    def create_post(self, post):
        cnx = self.connect()
        cursor = cnx.cursor()

        query = "INSERT INTO tblposts (title, content, published) VALUES (%s, %s, %s)"
        values = (post.title, post.content, post.published)
        cursor.execute(query, values)
        cnx.commit()

        id = cursor.lastrowid

        cursor.execute(f"SELECT * FROM tblposts WHERE id = {id}")
        post = cursor.fetchone()

        cursor.close()
        cnx.close()

        return post

    def get_post(self, id):
        pass

    def update_post(self, id):
        pass

    def delete_post(self, id):
        pass
