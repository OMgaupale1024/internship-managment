Developer notes — DB collation & admin user

1) Collation issue (fixed)
- Problem: Mixed collations (utf8mb4_unicode_ci vs utf8mb4_0900_ai_ci) caused MySQL error 1267 when comparing/joining text columns.
- Fix applied:
  - Converted database and tables to utf8mb4_unicode_ci:
    ALTER DATABASE internship_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ALTER TABLE internship_db.users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ALTER TABLE internship_db.students CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ALTER TABLE internship_db.companies CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ALTER TABLE internship_db.internships CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ALTER TABLE internship_db.applications CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  - Added a runtime fallback in `models.get_connection()` to run:
    SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'
    This prevents transient errors when client/server defaults differ.

2) Admin user creation
- A temporary script was used to create an admin user (username: `nake`, password: `123456`). The helper script has been removed for security.
- To create or reset admin credentials safely, prefer using the app's password-reset flow or generate a bcrypt hash and update the `users` table via the MySQL client.

3) Password hash formats
- The app now supports both werkzeug pbkdf2 hashes and bcrypt hashes stored in the DB.
- `app.py` contains a `verify_password` helper that uses `bcrypt.checkpw` for bcrypt hashes (starting with `$2`) and falls back to werkzeug's verifier otherwise.

4) Front-end Applications component
- A cleaned Tailwind-styled React component was added at `src/components/Applications.jsx` with:
  - Responsive table wrapper (`overflow-x-auto`) and `min-w-full w-full table-auto` on the table
  - Consistent header/cell padding (`px-6 py-3` / `px-6 py-4`)
  - Case-insensitive filtering and searching
  - Date formatting via `toLocaleDateString`
  - Dropdown `z-50` to avoid overlap
  - Badge spacing `inline-block px-2 py-1 rounded`

5) Next recommended steps
- Remove any other helper scripts that contain secrets.
- If deploying to production, ensure MySQL server default collation is set consistently and use a production WSGI server.
- Rotate the `nake` password to a stronger one and delete any references to the plaintext password.

If you'd like, I can:
- Rotate the `nake` password now and update the DB (generate a new bcrypt hash and update the row), or
- Add the `Applications.jsx` into an existing React build step if you give me the path to your front-end entry.
