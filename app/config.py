import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PAGINATION_LIMIT = 10
    LOG_FILE = "app.log"

    @staticmethod
    def get_db_config(db_type):
        return {
            'host': os.getenv(f'{db_type.upper()}_DB_HOST'),
            'user': os.getenv(f'{db_type.upper()}_DB_USER'),
            'password': os.getenv(f'{db_type.upper()}_DB_PASSWORD'),
            'database': os.getenv(f'{db_type.upper()}_DB_NAME')
        }