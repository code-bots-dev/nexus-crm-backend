import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class PostgreSQLConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(DATABASE_URL)

        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None