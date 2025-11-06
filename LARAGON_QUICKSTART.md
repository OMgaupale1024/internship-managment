# 🚀 Laragon Quick Start Guide

## Step-by-Step Setup in Laragon

### Step 1: Start Laragon MySQL

1. Open **Laragon**
2. Make sure MySQL is **running** (green icon)
3. If not running, click **Start All** button

### Step 2: Create the Database

**Option A: Using HeidiSQL (Easiest)**

1. In Laragon, click **Menu** → **Database** → **HeidiSQL**
2. Click **New** connection (or use existing)
   - Host: `127.0.0.1` or `localhost`
   - User: `root`
   - Password: Leave **1024** (Laragon default)
   - Port: `3306`
3. Click **Open**
4. Go to **File** → **Load SQL file**
5. Browse to your project folder and select `database_setup.sql`
6. Click **Execute** (F9) or click the **Play** button ▶️
7. Wait for success message

**Option B: Using MySQL Workbench**

1. Open MySQL Workbench
2. Create connection:
   - Hostname: `127.0.0.1`
   - Port: `3306`
   - Username: `root`
   - Password: Leave **empty** (or enter your Laragon MySQL password)
3. Connect
4. Open `database_setup.sql`
5. Execute (⚡ button)

### Step 3: Update config.py

Your `config.py` is already set for Laragon (empty password by default).

**If your Laragon MySQL has a password**, edit `config.py` line 12:
```python
"password": "your_password_here",
```

### Step 4: Install Dependencies

Open terminal in your project folder and run:

```bash
pip install -r requirements.txt
```

### Step 5: Fix Admin User

Run this to create/update admin user:

```bash
python fix_admin.py
```

### Step 6: Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 7: Access the App

Open browser: **http://localhost:5000**

**Login:**
- Username: `admin`
- Password: `1024`

---

## 🎯 Quick Checklist

- [ ] Laragon MySQL is running
- [ ] Database `internship_db` is created (run `database_setup.sql`)
- [ ] `config.py` has correct MySQL password (empty for Laragon default)
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Admin user fixed (`python fix_admin.py`)
- [ ] Flask app running (`python app.py`)
- [ ] Can login at http://localhost:5000

---

## 🔧 Troubleshooting

### "Unknown database 'internship_db'"
**Fix:** Run `database_setup.sql` in HeidiSQL or MySQL Workbench

### "Can't connect to MySQL server"
**Fix:** 
1. Make sure Laragon MySQL is running (green icon)
2. Check `config.py` password (try empty string `''`)

### "Access denied for user 'root'"
**Fix:** Check your MySQL password in `config.py`

### Admin login doesn't work
**Fix:** Run `python fix_admin.py`

---

## 📊 Viewing Data in Laragon

### Using HeidiSQL

1. Laragon → **Menu** → **Database** → **HeidiSQL**
2. Connect to MySQL
3. Select `internship_db` database
4. Double-click any table to view data
5. Right-click → **Refresh** to see updates

---

**That's it! You're ready to go! 🎉**

