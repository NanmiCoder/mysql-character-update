import os

from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Character set configuration
CHARSET = os.getenv("DB_CHARSET", "utf8mb4")
COLLATION = os.getenv("DB_COLLATION", "utf8mb4_general_ci")
ROW_FORMAT = os.getenv("DB_ROW_FORMAT", "Dynamic")

# Table filtering
VIEW_PREFIX = os.getenv("VIEW_PREFIX", "v_")

# Field types that need charset update
FIELD_TYPES_TO_UPDATE = os.getenv(
    "FIELD_TYPES_TO_UPDATE",
    "longtext,text,tinytext,char,varchar,json,mediumtext"
).lower().split(",")

# Execution mode
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
