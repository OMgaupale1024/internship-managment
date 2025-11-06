# Internship Management System - Setup Guide

This guide will help you set up the Internship Management System with MySQL database and connect it to MySQL Workbench.

## Prerequisites

1. **Python 3.8+** installed on your system
2. **MySQL Server** installed and running
3. **MySQL Workbench** installed (optional, but recommended for database management)

## Step 1: Install Python Dependencies

1. Open a terminal/command prompt in the project directory
2. Install required packages:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Flask>=2.0 mysql-connector-python>=8.0
```

## Step 2: Configure MySQL Database

### Option A: Using MySQL Workbench (Recommended)

1. **Open MySQL Workbench** and connect to your MySQL server
2. **Create a new connection** if needed:
   - Click the "+" icon next to "MySQL Connections"
   - Enter connection details:
     - Connection Name: `Internship DB`
     - Hostname: `localhost` (or your MySQL server IP)
     - Port: `3306`
     - Username: `root` (or your MySQL username)
     - Password: Click "Store in Keychain" and enter your password
   - Click "Test Connection" to verify
   - Click "OK" to save

3. **Run the database setup script**:
   - In MySQL Workbench, go to `File` → `Open SQL Script`
   - Navigate to the project folder and select `database_setup.sql`
   - Click the "Execute" button (⚡ lightning icon) or press `Ctrl+Shift+Enter`
   - Wait for the script to complete successfully

### Option B: Using Command Line

1. Open terminal/command prompt
2. Log in to MySQL:
   ```bash
   mysql -u root -p
   ```
   (Enter your MySQL password when prompted)

3. Run the setup script:
   ```bash
   source /path/to/database_setup.sql
   ```
   Or:
   ```bash
   mysql -u root -p < database_setup.sql
   ```

## Step 3: Configure Application Database Connection

1. Open `config.py` in your project directory
2. Update the database configuration:

```python
DB_CONFIG = {
    "host": "localhost",        # Your MySQL host (usually 'localhost')
    "user": "root",             # Your MySQL username
    "password": "YOUR_PASSWORD", # Your MySQL password
    "database": "internship_db", # Database name (should match database_setup.sql)
    "port": 3306,              # MySQL port (usually 3306)
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}
```

**Important**: Replace `YOUR_PASSWORD` with your actual MySQL root password.

Alternatively, you can set environment variables:
- `DB_HOST` (default: localhost)
- `DB_USER` (default: root)
- `DB_PASSWORD` (default: 1024)
- `DB_NAME` (default: internship_db)
- `DB_PORT` (default: 3306)

## Step 4: Run the Application

1. In your terminal, navigate to the project directory
2. Run the Flask application:

```bash
python app.py
```

3. You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

4. Open your web browser and go to: `http://localhost:5000`

## Step 5: Access MySQL Workbench to View Data

### Viewing Data in MySQL Workbench

1. **Open MySQL Workbench** and connect to your MySQL server
2. **Select the database**:
   - In the left sidebar, expand "Schemas"
   - Click on `internship_db` to select it
   - Tables will appear under it

3. **View table data**:
   - Double-click on any table (e.g., `students`, `companies`, `internships`, `applications`, `users`)
   - Click the "Table Data" tab at the bottom
   - You'll see all the data in that table

4. **Refresh data after changes**:
   - After making changes in the web application, click the "Refresh" button (🔄) in MySQL Workbench
   - Or right-click on the table and select "Refresh All"

### Running Queries in MySQL Workbench

1. Click on "Query" → "New Query Tab" (or press `Ctrl+T`)
2. Type your SQL query, for example:
   ```sql
   SELECT * FROM students;
   SELECT * FROM companies;
   SELECT * FROM internships;
   SELECT * FROM applications;
   ```
3. Click the "Execute" button (⚡) or press `Ctrl+Enter`
4. Results will appear in the bottom panel

### Monitoring Real-time Changes

1. **Keep MySQL Workbench open** while using the web application
2. **After each action** in the web app (add student, create internship, etc.):
   - Go back to MySQL Workbench
   - Right-click on the relevant table
   - Select "Refresh All"
   - View the updated data

3. **For automatic refresh**, you can:
   - Set up a query that runs periodically (Tools → Server Status)
   - Use the "Refresh" button manually after each change

## Step 6: Default Login Credentials

After running `database_setup.sql`, you can use these test accounts:

### Admin Account
- **Username**: `admin`
- **Password**: `1024`
- **Role**: Admin (full access)

### Company Account
- **Username**: `acme_corp` or `beta_solutions`
- **Password**: `1024`
- **Role**: Company

### Student Account
- **Username**: `aman_v` or `neha_s`
- **Password**: `1024`
- **Role**: Student

**⚠️ IMPORTANT**: Change these passwords in production!

## Troubleshooting

### Database Connection Errors

**Error**: `Access denied for user 'root'@'localhost'`
- **Solution**: Check your MySQL username and password in `config.py`
- Verify MySQL server is running: `sudo service mysql start` (Linux) or check Services (Windows)

**Error**: `Unknown database 'internship_db'`
- **Solution**: Run `database_setup.sql` script first to create the database

**Error**: `Can't connect to MySQL server`
- **Solution**: 
  - Verify MySQL server is running
  - Check if the host/port in `config.py` is correct
  - Ensure MySQL is accessible (check firewall settings)

### Python/Flask Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Error**: `Port 5000 already in use`
- **Solution**: 
  - Stop the other application using port 5000
  - Or change the port in `app.py`: `app.run(debug=True, port=5001)`

### MySQL Workbench Connection Issues

**Can't connect to MySQL server**
- Verify MySQL server is running
- Check connection settings (host, port, username, password)
- Ensure MySQL allows connections from your IP address

**Tables not showing data**
- Make sure you've selected the `internship_db` database
- Refresh the table (right-click → Refresh All)
- Check if data was actually inserted (run `SELECT * FROM table_name;`)

## Database Schema Overview

The application uses the following tables:

1. **users** - User authentication (username, password, email, role)
2. **students** - Student information (name, email, phone, branch)
3. **companies** - Company information (name, contact person, email, phone)
4. **internships** - Internship postings (title, company, dates, stipend, seats)
5. **applications** - Student applications (student, internship, status)

## Syncing Data Between Web App and MySQL Workbench

### How Data Sync Works

1. **All changes are real-time**: When you create, update, or delete data in the web application, it immediately updates the MySQL database.

2. **View changes in MySQL Workbench**:
   - Open MySQL Workbench
   - Connect to your database
   - Navigate to `internship_db` → `Tables`
   - Right-click on a table → Select "Select Rows - Limit 1000"
   - Or use the "Refresh" button after making changes

3. **Best Practice**:
   - Keep MySQL Workbench open in one window
   - Use the web app in another window
   - After each action in the web app, refresh the table view in MySQL Workbench

### Verifying Data Changes

1. **Create a new student** in the web app
2. **Go to MySQL Workbench**
3. **Right-click on `students` table** → "Select Rows - Limit 1000"
4. **You should see the new student** in the results

### Direct Database Changes

**You can also modify data directly in MySQL Workbench**:
- Changes made in MySQL Workbench will be reflected in the web application
- Be careful with foreign key constraints
- Use transactions for complex changes

## Next Steps

1. **Change default passwords** for security
2. **Create your own user accounts** through the registration page
3. **Customize the application** as needed
4. **Set up email notifications** (configure SMTP in `app.py`)

## Support

If you encounter any issues:
1. Check the error messages in the terminal/console
2. Verify MySQL server is running
3. Check database connection settings
4. Review the troubleshooting section above

---

**Happy Coding! 🚀**

