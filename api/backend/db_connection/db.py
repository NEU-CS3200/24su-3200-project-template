import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class DB:
    def __init__(self):
        self.db = None

    def get_db(self):
        if self.db is None or not self.db.is_connected():
            try:
                self.db = mysql.connector.connect(
                    host=os.getenv("DB_HOST", "db"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", "1234"),
                    database=os.getenv("DB_NAME", "fithub"),
                    autocommit=False,
                    auth_plugin='mysql_native_password'
                )
            except mysql.connector.errors.NotSupportedError:
                # If mysql_native_password doesn't work, try without auth_plugin
                # (for newer mysql-connector-python versions that support caching_sha2_password)
                self.db = mysql.connector.connect(
                    host=os.getenv("DB_HOST", "db"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", "1234"),
                    database=os.getenv("DB_NAME", "fithub"),
                    autocommit=False
                )
        return self.db

db = DB()
