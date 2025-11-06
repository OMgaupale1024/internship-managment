# Internship Management System (Flask + MySQL)

This is a simple internship management system built using Python (Flask) and MySQL. It implements core entities (students, companies, internships, applications) with CRUD operations and a Bootstrap UI. The app demonstrates database connectivity and dynamic updates (forms change the DB).

Prerequisites
- Python 3.8+
- MySQL Server

Quick setup
1. Clone or place the project folder and cd into it.
2. Create the database and tables by running the `db_init.sql` script. From a MySQL client (or Workbench):

   - Open PowerShell and run (adjust path if needed):

```
mysql -u root -p < "c:\Users\ogaup\OneDrive\Desktop\dbms\db_init.sql"
```

3. Edit `config.py` and set your MySQL credentials (user, password, host, port).
4. Install Python dependencies:

```
python -m pip install -r requirements.txt
```

5. Run the app:

```
python app.py
```

Open http://127.0.0.1:5000/ in the browser. Use the navbar to access Students, Companies, Internships, and Applications. Adding/editing via the UI will update the MySQL database.

Notes & next steps
- This is a scaffold focusing on functionality and clarity. You can extend it with authentication, validations, pagination, advanced SQL (reports, aggregate queries), role-based access, and nicer UX (AJAX edits without reloads).

Working with MySQL Workbench
- Open MySQL Workbench and connect to your MySQL server.
- Open the SQL file `static/sql/sample_ddls.sql` or `db_init.sql` in Workbench (File -> Open SQL Script) and run it to create tables / alter schema.
- Use `sample_dmls.sql` to practice INSERT/UPDATE/DELETE and aggregation queries.
- Use `sample_procs.sql` to create stored procedures (MySQL stored procedures). Note: PL/SQL is Oracle-specific; in MySQL use stored procedures.

Using the Labs page in the app
- Visit `/labs` (e.g. http://127.0.0.1:5000/labs) to see course-related examples and a safe query runner. The runner allows only read-only statements (SELECT/SHOW/EXPLAIN) from the browser for safety.
- For DDL/DML/DCL and stored procedure creation, prefer running the SQL in Workbench or using the provided SQL files.

Sync behavior (web UI <-> database)
- The web UI uses AJAX and calls the Flask API endpoints which execute SQL against the MySQL database. Any changes made through the web UI (add/edit/delete) are committed to the database immediately.
- Conversely, if you change data or schema directly in MySQL Workbench, the app will reflect those data changes on the next request (or immediately for the labs query tool). If you change schema (add/remove columns), you may need to update the app templates or restart the Flask server in some cases.

Safety and notes about destructive queries
- The web app's interactive query runner only allows read-only queries for safety. To run DDL/DML statements use Workbench or run SQL scripts from a trusted environment.

Admin user (demo)
- When the app starts for the first time it will create a default admin user if no users exist: username `admin` password `admin123`. Change this password immediately in production or before demonstrating.

Creating a read-only user for demonstration
- Use the script `static/sql/create_readonly_user.sql` to create a read-only MySQL user that can be used in MySQL Workbench for SELECT-only demonstrations.

