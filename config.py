"""Configuration for database connection. Edit these values for your MySQL instance."""
"""Configuration for database connection. Values can be overridden with environment variables.
Edit or set environment variables: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
"""
import os

DB_CONFIG = {
    "host": os.environ.get('DB_HOST', 'localhost'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', '1024'),
    "database": os.environ.get('DB_NAME', 'internship_db'),
    "port": int(os.environ.get('DB_PORT', 3306)),
    "charset": 'utf8mb4',
    "collation": 'utf8mb4_unicode_ci'
}
