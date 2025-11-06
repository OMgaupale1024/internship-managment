"""Laragon-specific database configuration.
Laragon MySQL typically uses empty password by default.
Copy this to config.py if you're using Laragon, or update config.py with your Laragon MySQL password.
"""
import os

DB_CONFIG = {
    "host": os.environ.get('DB_HOST', 'localhost'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', '1024'),  # Laragon default is usually empty
    "database": os.environ.get('DB_NAME', 'internship_db'),
    "port": int(os.environ.get('DB_PORT', 3306)),
    "charset": 'utf8mb4',
    "collation": 'utf8mb4_unicode_ci'
}

