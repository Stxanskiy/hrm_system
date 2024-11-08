import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
