@echo off
echo ============================================
echo Laragon Setup Script for Internship Management
echo ============================================
echo.

REM Check if MySQL is running in Laragon
echo [1/4] Checking Laragon MySQL...
echo Make sure Laragon MySQL is running (green icon in Laragon)
echo.

REM Install Python dependencies
echo [2/4] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Setup database
echo [3/4] Setting up database...
echo Please run database_setup.sql in HeidiSQL or MySQL Workbench
echo.
echo Instructions:
echo 1. Open Laragon
echo 2. Click Menu -^> Database -^> HeidiSQL
echo 3. Connect to MySQL
echo 4. File -^> Load SQL file
echo 5. Select database_setup.sql
echo 6. Click Execute (F9)
echo.

REM Fix admin user
echo [4/4] Fixing admin user...
python fix_admin.py
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Make sure database_setup.sql is executed
echo 2. Update config.py with your MySQL password (if Laragon has one)
echo 3. Run: python app.py
echo 4. Open: http://localhost:5000
echo.
echo Admin Login:
echo   Username: admin
echo   Password: 1024
echo.
pause

