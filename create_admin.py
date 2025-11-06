#!/usr/bin/env python3
# Helper to create an admin user in the local internship_db using config.DB_CONFIG
import sys
import subprocess
from werkzeug.security import generate_password_hash

try:
    import mysql.connector
except Exception:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mysql-connector-python'])
    import mysql.connector

from config import DB_CONFIG

username = 'nake'
password = '123456'
email = 'nake@gamil.com'
role = 'admin'

hashed = generate_password_hash(password)

print('Generated password hash for user', username)

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
try:
    cur.execute("INSERT INTO users (username, password_hash, email, role) VALUES (%s,%s,%s,%s)", (username, hashed, email, role))
    conn.commit()
    print('Inserted new user id:', cur.lastrowid)
except mysql.connector.Error as e:
    print('MySQL error:', e)
    sys.exit(1)
finally:
    cur.close()
    conn.close()
