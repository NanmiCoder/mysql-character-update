import os

DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "your db name")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your db password")
