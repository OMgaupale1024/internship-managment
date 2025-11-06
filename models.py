import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        # Ensure the connection uses a consistent charset and collation to avoid
        # "Illegal mix of collations" errors when the server or some tables use
        # a different default (e.g. utf8mb4_0900_ai_ci on MySQL 8.0).
        # We send an explicit SET NAMES with the desired collation as a fallback.
        try:
            cur = conn.cursor()
            cur.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'")
            cur.close()
        except Exception:
            # Don't fail the whole connection if the server doesn't accept the
            # statement for some reason; the higher-level code may still work
            # or the permanent fix is to alter the database/table collations.
            pass
        return conn
    except Error as e:
        raise

def fetchall(query, params=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def run_select(query):
    """Run a SELECT/SHOW/EXPLAIN style query and return rows.
    This helper performs a simple safety check to allow only read-only queries.
    """
    safe = query.strip().lower()
    # very basic safety: only allow read-only statements
    if not (safe.startswith('select') or safe.startswith('show') or safe.startswith('explain')):
        raise ValueError('Only read-only queries (SELECT/SHOW/EXPLAIN) are allowed via this method')
    return fetchall(query)


def get_tables():
    """Return a list of table names and approximate row counts for the configured database."""
    q = "SELECT table_name, table_rows FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name"
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(q, (DB_CONFIG['database'],))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Normalize
    out = []
    for r in rows:
        # information_schema may return uppercase keys; be resilient
        table = r.get('table_name') or r.get('TABLE_NAME') or r.get('Table_name')
        rows_count = r.get('table_rows') or r.get('TABLE_ROWS') or r.get('Table_rows') or 0
        out.append({'table': table, 'rows': rows_count})
    return out


def get_table_columns(table_name):
    """Return list of columns (name, type, nullable) for a table in the configured DB."""
    q = "SELECT column_name, data_type, is_nullable, column_key FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position"
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(q, (DB_CONFIG['database'], table_name))
    cols = cur.fetchall()
    cur.close()
    conn.close()
    # normalize keys in returned dicts for convenience
    norm = []
    for c in cols:
        norm.append({
            'column_name': c.get('column_name') or c.get('COLUMN_NAME') or c.get('Column_name'),
            'data_type': c.get('data_type') or c.get('DATA_TYPE') or c.get('Data_type'),
            'is_nullable': c.get('is_nullable') or c.get('IS_NULLABLE') or c.get('Is_nullable'),
            'column_key': c.get('column_key') or c.get('COLUMN_KEY') or c.get('Column_key'),
        })
    return norm


def get_table_sample(table_name, limit=10):
    """Return up to `limit` rows from `table_name`. Validates table exists first."""
    # Validate table exists
    tables = [t['table'] for t in get_tables()]
    if table_name not in tables:
        raise ValueError('Unknown table')
    # Build and execute safe query
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    # Note: table name cannot be parameterized, so validate above then use backticks
    q = f"SELECT * FROM `{table_name}` LIMIT %s"
    cur.execute(q, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def execute(query, params=None, commit=True):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    if commit:
        conn.commit()
    lastrowid = cur.lastrowid
    cur.close()
    conn.close()
    return lastrowid

# Students
def get_students():
    return fetchall("SELECT * FROM students ORDER BY id DESC")

def add_student(name, email, phone, branch):
    return execute(
        "INSERT INTO students (name, email, phone, branch) VALUES (%s,%s,%s,%s)",
        (name, email, phone, branch),
    )

def update_student(student_id, name, email, phone, branch):
    return execute(
        "UPDATE students SET name=%s, email=%s, phone=%s, branch=%s WHERE id=%s",
        (name, email, phone, branch, student_id),
    )

def delete_student(student_id):
    return execute("DELETE FROM students WHERE id=%s", (student_id,))

# Companies
def get_companies():
    return fetchall("SELECT * FROM companies ORDER BY id DESC")

def add_company(name, contact_person, email, phone):
    return execute(
        "INSERT INTO companies (name, contact_person, email, phone) VALUES (%s,%s,%s,%s)",
        (name, contact_person, email, phone),
    )

def update_company(company_id, name, contact_person, email, phone):
    return execute(
        "UPDATE companies SET name=%s, contact_person=%s, email=%s, phone=%s WHERE id=%s",
        (name, contact_person, email, phone, company_id),
    )

def delete_company(company_id):
    return execute("DELETE FROM companies WHERE id=%s", (company_id,))

# Internships
def get_internships():
    return fetchall(
        "SELECT i.*, c.name AS company_name FROM internships i LEFT JOIN companies c ON i.company_id = c.id ORDER BY i.id DESC"
    )

def add_internship(title, company_id, start_date, end_date, stipend, seats, description):
    return execute(
        "INSERT INTO internships (title, company_id, start_date, end_date, stipend, seats, description) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (title, company_id, start_date, end_date, stipend, seats, description),
    )

def update_internship(iid, title, company_id, start_date, end_date, stipend, seats, description):
    return execute(
        "UPDATE internships SET title=%s, company_id=%s, start_date=%s, end_date=%s, stipend=%s, seats=%s, description=%s WHERE id=%s",
        (title, company_id, start_date, end_date, stipend, seats, description, iid),
    )

def delete_internship(iid):
    return execute("DELETE FROM internships WHERE id=%s", (iid,))

# Applications
def get_applications():
    return fetchall(
        "SELECT a.*, s.name AS student_name, i.title AS internship_title FROM applications a LEFT JOIN students s ON a.student_id=s.id LEFT JOIN internships i ON a.internship_id=i.id ORDER BY a.id DESC"
    )

def add_application(student_id, internship_id, status='Applied'):
    return execute(
        "INSERT INTO applications (student_id, internship_id, status) VALUES (%s,%s,%s)",
        (student_id, internship_id, status),
    )

def update_application(app_id, status):
    return execute("UPDATE applications SET status=%s WHERE id=%s", (status, app_id))

def delete_application(app_id):
    return execute("DELETE FROM applications WHERE id=%s", (app_id,))


# User authentication and management
def get_user_by_username(username):
    rows = fetchall("SELECT * FROM users WHERE username = %s", (username,))
    return rows[0] if rows else None

def get_student_by_username(username):
    rows = fetchall("""
        SELECT s.* FROM students s 
        JOIN users u ON s.email = u.email 
        WHERE u.username = %s AND u.role = 'student'
    """, (username,))
    return rows[0] if rows else None

def get_company_by_username(username):
    rows = fetchall("""
        SELECT c.* FROM companies c 
        JOIN users u ON c.email = u.email 
        WHERE u.username = %s AND u.role = 'company'
    """, (username,))
    return rows[0] if rows else None

def get_company_internships(company_id):
    if not company_id:
        return []
    return fetchall("SELECT * FROM internships WHERE company_id = %s ORDER BY id DESC", (company_id,))

def get_company_applications(company_id):
    if not company_id:
        return []
    return fetchall("""
        SELECT a.*, s.name AS student_name, s.email AS student_email, i.title AS internship_title
        FROM applications a 
        LEFT JOIN students s ON a.student_id = s.id 
        LEFT JOIN internships i ON a.internship_id = i.id
        WHERE i.company_id = %s
        ORDER BY a.id DESC
    """, (company_id,))

def get_student_applications(student_id):
    if not student_id:
        return []
    return fetchall("""
        SELECT a.*, s.name AS student_name, s.email AS student_email, 
               i.title AS internship_title, c.name AS company_name
        FROM applications a 
        LEFT JOIN students s ON a.student_id = s.id 
        LEFT JOIN internships i ON a.internship_id = i.id
        LEFT JOIN companies c ON i.company_id = c.id
        WHERE a.student_id = %s
        ORDER BY a.id DESC
    """, (student_id,))

def get_user_by_email(email):
    rows = fetchall("SELECT * FROM users WHERE email = %s", (email,))
    return rows[0] if rows else None

def add_user(username, password_hash, email, role='student'):
    return execute(
        "INSERT INTO users (username, password_hash, email, role) VALUES (%s,%s,%s,%s)",
        (username, password_hash, email, role)
    )

def set_reset_token(email, token, expires_at):
    return execute(
        "UPDATE users SET reset_token = %s, reset_token_expires = %s WHERE email = %s",
        (token, expires_at, email)
    )

def get_user_by_reset_token(token):
    rows = fetchall(
        "SELECT * FROM users WHERE reset_token = %s AND reset_token_expires > NOW()",
        (token,)
    )
    return rows[0] if rows else None

def clear_reset_token(user_id):
    return execute(
        "UPDATE users SET reset_token = NULL, reset_token_expires = NULL WHERE id = %s",
        (user_id,)
    )

def update_password(user_id, password_hash):
    return execute(
        "UPDATE users SET password_hash = %s WHERE id = %s",
        (password_hash, user_id)
    )

def get_user_count():
    rows = fetchall("SELECT COUNT(*) AS cnt FROM users")
    return rows[0]['cnt'] if rows else 0

