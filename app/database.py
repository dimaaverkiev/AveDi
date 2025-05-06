import mysql.connector
from .config import Config

class Database:

    @staticmethod
    def get_connection(db_type='ich'):
        config = Config.get_db_config(db_type)

        try:
            return mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print(f"[✖] Database connection error: {err}")
            exit()

    @staticmethod
    def insert_search(text, search_type, connection, cursor):
        try:
            cursor.executemany('INSERT INTO search_counter (filter_text, filter_type, filter_counter) '
                                'VALUES ( %s , %s , 1) '
                                'ON DUPLICATE KEY UPDATE filter_counter = filter_counter + 1', [(text, search_type)])

            cursor.executemany('insert into search_history(filter_text, filter_type, filter_date) '
                                'values( %s , %s , curdate())', [(text, search_type)])

            connection.commit()

        except Exception as e:
            print(f"[✖] Error saving search: {e}")
            raise