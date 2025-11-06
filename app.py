from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
import models
import re
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from werkzeug.security import generate_password_hash, check_password_hash
def verify_password(stored_hash, password):
    """Verify a password against a stored hash using werkzeug.
    All passwords are stored using werkzeug's generate_password_hash (scrypt).
    """
    if not stored_hash:
        return False
    try:
        return check_password_hash(stored_hash, password)
    except (ValueError, TypeError):
        # If werkzeug cannot parse the hash, fail safely
        return False
import datetime

app = Flask(__name__)
app.secret_key = 'change_this_to_a_random_secret_in_prod'

def send_email(to_email, subject, body):
    """Send an email using SMTP. For demo, prints to console instead."""
    # In production, use real SMTP settings from environment variables
    print(f"\nEmail would be sent to: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")

def login_required(fn):
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def admin_required(fn):
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            return render_template('error.html', error='Access denied. Admin privileges required.')
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def company_required(fn):
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        if session.get('role') not in ['admin', 'company']:
            return render_template('error.html', error='Access denied. Company privileges required.')
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def ensure_admin():
    # create a default admin user if none exists, or update password if admin exists but can't login
    try:
        admin_user = models.get_user_by_username('admin')
        if not admin_user:
            # No admin exists, create one
            # default credentials: admin / 1024 (please change)
            pw = generate_password_hash('1024')
            try:
                models.add_user('admin', pw, 'admin@internship.com', role='admin')
                print('[SUCCESS] Created default admin user: username=admin password=1024')
            except Exception as e:
                print(f'[WARNING] Could not create admin user: {e}')
        else:
            # Admin exists, verify password works
            # If password verification fails, we'll update it
            if not verify_password(admin_user['password_hash'], '1024'):
                # Password doesn't match, update it
                pw = generate_password_hash('1024')
                models.update_password(admin_user['id'], pw)
                print('[SUCCESS] Updated admin password: username=admin password=1024')
    except Exception as e:
        # if users table doesn't exist or DB not ready, ignore here
        print(f'[WARNING] Could not ensure admin user exists: {e}')
        pass

@app.route('/')
@login_required
def index():
    role = session.get('role', 'student')
    username = session.get('user')
    
    if role == 'admin':
        students = models.get_students()
        companies = models.get_companies()
        internships = models.get_internships()
        applications = models.get_applications()
    elif role == 'company':
        students = []
        companies = [models.get_company_by_username(username)] if username else []
        internships = models.get_company_internships(companies[0]['id'] if companies else None)
        applications = models.get_company_applications(companies[0]['id'] if companies else None)
    else:  # student
        student = models.get_student_by_username(username)
        students = [student] if student else []
        companies = models.get_companies()
        internships = models.get_internships()
        applications = models.get_student_applications(student['id'] if student else None)
    
    return render_template('index.html', 
                         students=students, 
                         companies=companies, 
                         internships=internships, 
                         applications=applications,
                         role=role)

### Students endpoints
@app.route('/students')
@admin_required
def students_page():
    students = models.get_students()
    return render_template('students.html', students=students, role='admin')

@app.route('/api/students', methods=['POST'])
@admin_required
def api_add_student():
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    data = request.json or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    if not name:
        return jsonify({'status':'error','message':'Name is required'}), 400
    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({'status':'error','message':'Invalid email'}), 400
    sid = models.add_student(name, email or None, data.get('phone'), data.get('branch'))
    return jsonify({'status':'ok','id': sid})

@app.route('/api/students/<int:sid>', methods=['PUT','DELETE'])
def api_student_modify(sid):
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    if request.method == 'PUT':
        data = request.json or {}
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip()
        if not name:
            return jsonify({'status':'error','message':'Name is required'}), 400
        if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return jsonify({'status':'error','message':'Invalid email'}), 400
        models.update_student(sid, name, email or None, data.get('phone'), data.get('branch'))
        return jsonify({'status':'ok'})
    else:
        models.delete_student(sid)
        return jsonify({'status':'ok'})

### Companies endpoints
@app.route('/companies')
def companies_page():
    companies = models.get_companies()
    return render_template('companies.html', companies=companies)

@app.route('/api/companies', methods=['POST'])
def api_add_company():
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    data = request.json or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'status':'error','message':'Name is required'}), 400
    cid = models.add_company(name, data.get('contact_person'), data.get('email'), data.get('phone'))
    return jsonify({'status':'ok','id': cid})

@app.route('/api/companies/<int:cid>', methods=['PUT','DELETE'])
def api_company_modify(cid):
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    if request.method == 'PUT':
        data = request.json or {}
        name = (data.get('name') or '').strip()
        if not name:
            return jsonify({'status':'error','message':'Name is required'}), 400
        models.update_company(cid, name, data.get('contact_person'), data.get('email'), data.get('phone'))
        return jsonify({'status':'ok'})
    else:
        models.delete_company(cid)
        return jsonify({'status':'ok'})

### Internships endpoints
@app.route('/internships')
def internships_page():
    internships = models.get_internships()
    companies = models.get_companies()
    return render_template('internships.html', internships=internships, companies=companies)

@app.route('/api/internships', methods=['POST'])
def api_add_internship():
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    data = request.json or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'status':'error','message':'Title is required'}), 400
    iid = models.add_internship(title, data.get('company_id'), data.get('start_date'), data.get('end_date'), data.get('stipend'), data.get('seats'), data.get('description'))
    return jsonify({'status':'ok','id': iid})

@app.route('/api/internships/<int:iid>', methods=['PUT','DELETE'])
def api_internship_modify(iid):
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    if request.method == 'PUT':
        data = request.json or {}
        title = (data.get('title') or '').strip()
        if not title:
            return jsonify({'status':'error','message':'Title is required'}), 400
        models.update_internship(iid, title, data.get('company_id'), data.get('start_date'), data.get('end_date'), data.get('stipend'), data.get('seats'), data.get('description'))
        return jsonify({'status':'ok'})
    else:
        models.delete_internship(iid)
        return jsonify({'status':'ok'})

### Applications
@app.route('/applications')
def applications_page():
    applications = models.get_applications()
    students = models.get_students()
    internships = models.get_internships()
    return render_template('applications.html', applications=applications, students=students, internships=internships)


@app.route('/labs')
def labs_page():
    """A small page with course-related SQL examples and a safe query runner (SELECT only)."""
    examples = {
        'ddl_create_table': 'CREATE TABLE sample_demo (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100));',
        'dml_insert': "INSERT INTO students (name, email, phone, branch) VALUES ('Test Student','test@example.com','+911234567890','CSE');",
        'dml_update': "UPDATE students SET branch='IT' WHERE id=1;",
        'dcl_grant': "GRANT SELECT ON internship_db.* TO 'someuser'@'localhost';",
        'advanced_join': 'SELECT s.name AS student, i.title AS internship FROM applications a JOIN students s ON a.student_id=s.id JOIN internships i ON a.internship_id=i.id;',
        'aggregate': 'SELECT i.title, COUNT(a.id) AS applications FROM internships i LEFT JOIN applications a ON a.internship_id=i.id GROUP BY i.id;'
    }
    return render_template('labs.html', examples=examples)


@app.route('/db')
def db_view():
    """Render a simple database browser showing each table and a small sample of rows."""
    if not session.get('user'):
        return redirect(url_for('login'))
    tables = models.get_tables()
    table_data = []
    for t in tables:
        name = t.get('table')
        try:
            cols = models.get_table_columns(name)
            sample = models.get_table_sample(name, limit=5)
            # stringify datetimes for safe rendering
            for r in sample:
                for k, v in list(r.items()):
                    if isinstance(v, (datetime.date, datetime.datetime)):
                        r[k] = str(v)
        except Exception as e:
            cols = []
            sample = []
        table_data.append({'table': name, 'rows': t.get('rows', 0), 'columns': cols, 'sample': sample})
    return render_template('db_view.html', tables=table_data)


@app.route('/api/query', methods=['POST'])
def api_run_query():
    """Run a read-only SQL query (SELECT/SHOW/EXPLAIN) and return results.
    This endpoint intentionally rejects non-read queries to avoid destructive changes via UI.
    """
    data = request.json or {}
    query = data.get('query','').strip()
    if not query:
        return jsonify({'status':'error','message':'No query provided'}), 400
    try:
        rows = models.run_select(query)
        return jsonify({'status':'ok','rows': rows})
    except ValueError as ve:
        return jsonify({'status':'error','message': str(ve)}), 400
    except Exception as e:
        return jsonify({'status':'error','message': 'Query failed: '+str(e)}), 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.form
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    confirm = data.get('confirm_password') or ''
    email = (data.get('email') or '').strip()
    account_type = data.get('account_type')
    
    if not username or not password or not confirm or not email or not account_type:
        return render_template('register.html', error='All fields are required')
    
    if len(password) < 6:
        return render_template('register.html', error='Password must be at least 6 characters long')
    
    if password != confirm:
        return render_template('register.html', error='Passwords do not match')
        
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return render_template('register.html', error='Invalid email address')
    
    # Check if username exists
    if models.get_user_by_username(username):
        return render_template('register.html', error='Username already exists')
    
    # Check if email exists
    if models.get_user_by_email(email):
        return render_template('register.html', error='Email already registered')
    
    # Create user
    try:
        pw_hash = generate_password_hash(password)
        # Create user account
        models.add_user(username, pw_hash, email, role=account_type)

        # Create corresponding student or company record
        if account_type == 'student':
            student_name = data.get('student_name') or username
            student_phone = data.get('student_phone')
            student_branch = data.get('student_branch')
            try:
                models.add_student(student_name, email, student_phone, student_branch)
            except Exception as e:
                # If student creation fails, continue anyway (user can update profile later)
                print(f"Warning: Could not create student record: {e}")
        
        elif account_type == 'company':
            company_name = data.get('company_name') or username
            contact_person = data.get('contact_person')
            company_phone = data.get('company_phone')
            try:
                models.add_company(company_name, contact_person, email, company_phone)
            except Exception as e:
                # If company creation fails, continue anyway (user can update profile later)
                print(f"Warning: Could not create company record: {e}")

        # Log them in
        session['user'] = username
        session['role'] = account_type

        # Send welcome email
        send_email(
            email,
            "Welcome to Internship Management System",
            f"Hi {username},\n\nWelcome to the Internship Management System. Your {account_type} account has been created successfully."
        )

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Registration error: {e}")
        return render_template('register.html', error=f'Registration failed: {str(e)}')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot-password.html')
    
    email = (request.form.get('email') or '').strip()
    if not email:
        return render_template('forgot-password.html', error='Email is required')
    
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return render_template('forgot-password.html', error='Invalid email address')
    
    # For demo, just print reset instructions
    # In production, generate a secure token and send a real email
    send_email(
        email,
        "Password Reset Instructions",
        "A password reset was requested. If this wasn't you, please ignore this email."
    )
    
    return render_template('forgot-password.html', 
        success='If an account exists with that email, you will receive reset instructions shortly')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.form
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return render_template('login.html', error='username and password required')
    user = models.get_user_by_username(username)
    if not user:
        return render_template('login.html', error='invalid credentials')
    # Support multiple hash formats (werkzeug pbkdf2 or bcrypt hashes stored by
    # other utilities). verify_password will return False on mismatch or
    # unsupported formats.
    if not verify_password(user['password_hash'], password):
        return render_template('login.html', error='invalid credentials')
    session['user'] = user['username']
    session['role'] = user.get('role', 'user')  # Store role in session
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    role = session.get('role', 'student')
    username = session.get('user')
    
    if role == 'student':
        profile_data = models.get_student_by_username(username)
        if not profile_data:
            return render_template('error.html', error='Student profile not found')
            
        if request.method == 'POST':
            models.update_student(
                profile_data['id'],
                request.form.get('name'),
                request.form.get('email'),
                request.form.get('phone'),
                request.form.get('branch')
            )
            return redirect(url_for('profile'))
            
    elif role == 'company':
        profile_data = models.get_company_by_username(username)
        if not profile_data:
            return render_template('error.html', error='Company profile not found')
            
        if request.method == 'POST':
            models.update_company(
                profile_data['id'],
                request.form.get('name'),
                request.form.get('contact_person'),
                request.form.get('email'),
                request.form.get('phone')
            )
            return redirect(url_for('profile'))
    else:
        return render_template('error.html', error='Invalid user type')
    
    return render_template('profile.html', profile=profile_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/api/table_export/<table_name>')
def api_table_export(table_name):
    # Require login to export
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    try:
        rows = models.get_table_sample(table_name, limit=10000)
        if not rows:
            return jsonify({'status':'error','message':'No rows to export'}), 400
        # build CSV
        def generate():
            header = list(rows[0].keys())
            out = csv.StringIO()
            writer = csv.writer(out)
            writer.writerow(header)
            yield out.getvalue()
            out.seek(0); out.truncate(0)
            for r in rows:
                writer.writerow([r.get(c) for c in header])
                yield out.getvalue()
                out.seek(0); out.truncate(0)
        disp = f'attachment; filename="{table_name}.csv"'
        return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': disp})
    except Exception as e:
        return jsonify({'status':'error','message': str(e)}), 500


@app.route('/api/db_overview')
def api_db_overview():
    """Return tables and their columns for the configured database."""
    try:
        tables = models.get_tables()
        result = []
        for t in tables:
            cols = models.get_table_columns(t['table'])
            result.append({'table': t['table'], 'rows': t.get('rows', 0), 'columns': cols})
        return jsonify({'status':'ok','tables': result})
    except Exception as e:
        return jsonify({'status':'error','message': str(e)}), 500


@app.route('/api/table_sample/<table_name>')
def api_table_sample(table_name):
    limit = request.args.get('limit', 10, type=int)
    try:
        rows = models.get_table_sample(table_name, limit=limit)
        # convert non-JSON types to strings where necessary
        import datetime
        safe_rows = []
        for r in rows:
            safe = {}
            for k, v in r.items():
                if isinstance(v, (datetime.date, datetime.datetime)):
                    safe[k] = str(v)
                else:
                    safe[k] = v
            safe_rows.append(safe)
        return jsonify({'status':'ok','rows': safe_rows})
    except ValueError as ve:
        return jsonify({'status':'error','message': str(ve)}), 400
    except Exception as e:
        return jsonify({'status':'error','message': str(e)}), 500

@app.route('/api/applications', methods=['POST'])
def api_add_application():
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    data = request.json or {}
    sid = data.get('student_id')
    iid = data.get('internship_id')
    if not sid or not iid:
        return jsonify({'status':'error','message':'student_id and internship_id are required'}), 400
    aid = models.add_application(sid, iid)
    return jsonify({'status':'ok','id':aid})

@app.route('/api/applications/<int:aid>', methods=['PUT','DELETE'])
def api_application_modify(aid):
    if not session.get('user'):
        return jsonify({'status':'error','message':'Authentication required'}), 401
    if request.method == 'PUT':
        data = request.json or {}
        status = data.get('status') or 'Applied'
        models.update_application(aid, status)
        return jsonify({'status':'ok'})
    else:
        models.delete_application(aid)
        return jsonify({'status':'ok'})

if __name__ == '__main__':
    # ensure default admin exists before handling requests (some Flask builds may not have
    # the before_first_request decorator available). This call is safe because the function
    # already handles DB-not-ready exceptions.
    try:
        ensure_admin()
    except Exception:
        pass
    app.run(debug=True)
