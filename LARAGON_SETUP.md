# Laragon Setup Guide for Internship Management System

This guide will help you set up the Flask application in Laragon on Windows.

## Prerequisites

1. **Laragon** installed and running
2. **Python 3.8+** installed (may be separate from Laragon)
3. **MySQL** should be running in Laragon

## Step 1: Configure Laragon MySQL

### Check Laragon MySQL Settings

1. Open **Laragon**
2. Click **Menu** → **MySQL** → **Config** → **my.ini** (or check Laragon settings)
3. Note the MySQL port (usually **3306**)
4. Check if MySQL root password is set (Laragon default is usually **empty/blank**)

### Access MySQL in Laragon

1. In Laragon, click **Menu** → **Database** → **HeidiSQL** (or use MySQL Workbench)
2. Or use terminal: `mysql -u root -p` (press Enter if password is blank)

## Step 2: Update Database Configuration

Edit `config.py` to match Laragon's MySQL settings:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Laragon default is usually empty
    "database": "internship_db",
    "port": 3306,
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}
```

**Important**: If your Laragon MySQL has a password, update it in `config.py`.

## Step 3: Set Up the Database

### Option A: Using HeidiSQL (Laragon's Built-in Tool)

1. In Laragon, click **Menu** → **Database** → **HeidiSQL**
2. Connect to MySQL (root user, password if set)
3. Go to **File** → **Load SQL file**
4. Select `database_setup.sql` from your project folder
5. Click **Execute** (F9) or click the **Play** button
6. Wait for "Query OK" messages

### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Create a new connection:
   - Hostname: `localhost`
   - Port: `3306`
   - Username: `root`
   - Password: (leave blank if Laragon default, or enter your password)
3. Connect to the server
4. Open `database_setup.sql` in Workbench
5. Execute the script

### Option C: Using Command Line

1. Open **Laragon Terminal** (or CMD/PowerShell)
2. Navigate to your project folder:
   ```bash
   cd "C:\laragon\www\internship-management"
   ```
   (Adjust path to your actual project location)

3. Run:
   ```bash
   mysql -u root -p < database_setup.sql
   ```
   (Press Enter if password prompt appears, or enter your MySQL password)

## Step 4: Install Python Dependencies

1. Open **Laragon Terminal** or any terminal
2. Navigate to your project folder:
   ```bash
   cd "C:\laragon\www\internship-management"
   ```
   (Adjust to your actual project location)

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Or install manually:
```bash
pip install Flask>=2.0 mysql-connector-python>=8.0
```

## Step 5: Fix Admin User (If Needed)

If you can't log in as admin, run:

```bash
python fix_admin.py
```

This will create/update the admin user with:
- Username: `admin`
- Password: `1024`

## Step 6: Run the Flask Application

### Option A: Direct Python (Recommended for Development)

1. Open terminal in your project folder
2. Run:
   ```bash
   python app.py
   ```

3. You should see:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

4. Open browser: `http://localhost:5000`

### Option B: Using Laragon's Terminal

1. In Laragon, click **Terminal** button
2. Navigate to project:
   ```bash
   cd www\internship-management
   ```
3. Run:
   ```bash
   python app.py
   ```

## Step 7: Verify Database Connection

1. **Start Flask app** (see Step 6)
2. **Open HeidiSQL** or **MySQL Workbench**
3. Connect to MySQL
4. Select `internship_db` database
5. Check tables: `users`, `students`, `companies`, `internships`, `applications`
6. View data in tables

## Troubleshooting

### MySQL Connection Error

**Error**: `Can't connect to MySQL server`

**Solutions**:
1. Make sure Laragon MySQL is running (green icon in Laragon)
2. Check `config.py` - password might be wrong (try empty string `""`)
3. Verify MySQL port (usually 3306)
4. In Laragon, click **Menu** → **MySQL** → **Start** if not running

### Port Already in Use

**Error**: `Port 5000 already in use`

**Solutions**:
1. Change port in `app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```
2. Or stop other applications using port 5000

### Database Not Found

**Error**: `Unknown database 'internship_db'`

**Solution**: Run `database_setup.sql` script (see Step 3)

### Admin Login Issues

**Solution**: Run `python fix_admin.py` to reset admin password

### Python Not Found

**Error**: `python: command not found`

**Solutions**:
1. Use `py` instead of `python`:
   ```bash
   py app.py
   ```
2. Or use full path to Python:
   ```bash
   C:\Python310\python.exe app.py
   ```
3. Make sure Python is in your PATH

## Laragon Project Structure (Optional)

You can organize your project in Laragon's www folder:

```
C:\laragon\www\
└── internship-management\
    ├── app.py
    ├── config.py
    ├── models.py
    ├── database_setup.sql
    ├── templates\
    ├── static\
    └── ...
```

## Accessing the Application

Once running, access the app at:
- **URL**: `http://localhost:5000`
- **Login**: `admin` / `1024`

## Viewing Data in Laragon

### Using HeidiSQL

1. In Laragon, click **Menu** → **Database** → **HeidiSQL**
2. Connect to MySQL
3. Select `internship_db` database
4. Double-click any table to view data
5. Right-click table → **Refresh** to see updates

### Using MySQL Workbench

1. Connect to `localhost:3306`
2. Select `internship_db` schema
3. View table data

## Next Steps

1. ✅ Database is set up
2. ✅ Admin user is created
3. ✅ Flask app is running
4. ✅ You can now:
   - Register new users
   - Create students/companies
   - Post internships
   - Manage applications

## Quick Reference

| Item | Value |
|------|-------|
| **MySQL Host** | `localhost` |
| **MySQL Port** | `3306` |
| **MySQL User** | `root` |
| **MySQL Password** | Usually empty in Laragon |
| **Database Name** | `internship_db` |
| **Flask URL** | `http://localhost:5000` |
| **Admin Username** | `admin` |
| **Admin Password** | `1024` |

---

**Happy Coding! 🚀**

