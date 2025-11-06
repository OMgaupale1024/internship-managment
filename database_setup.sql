-- ============================================
-- Internship Management System Database Setup
-- ============================================
-- This script creates the database and all required tables
-- Run this in MySQL Workbench or command line to set up the database
-- ============================================

-- Drop existing database if it exists (uncomment if you want to reset)
-- DROP DATABASE IF EXISTS internship_db;

-- Create database with proper charset and collation
CREATE DATABASE IF NOT EXISTS internship_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE internship_db;

-- ============================================
-- Students Table
-- ============================================
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(50),
  branch VARCHAR(120),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Companies Table
-- ============================================
CREATE TABLE IF NOT EXISTS companies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  contact_person VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Internships Table
-- ============================================
CREATE TABLE IF NOT EXISTS internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  company_id INT,
  start_date DATE,
  end_date DATE,
  stipend VARCHAR(100),
  seats INT DEFAULT 1,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL ON UPDATE CASCADE,
  INDEX idx_company_id (company_id),
  INDEX idx_start_date (start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Applications Table
-- ============================================
CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT,
  internship_id INT,
  status VARCHAR(50) DEFAULT 'Applied',
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_student_id (student_id),
  INDEX idx_internship_id (internship_id),
  INDEX idx_status (status),
  UNIQUE KEY unique_application (student_id, internship_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Users Table (Authentication)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'student',
  reset_token VARCHAR(255),
  reset_token_expires TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Sample Data (Optional - for testing)
-- ============================================
-- Default admin user (username: admin, password: 1024)
-- Note: Change this password immediately in production!
-- Using werkzeug hash (scrypt) - no bcrypt needed
INSERT IGNORE INTO users (username, password_hash, email, role) VALUES
('admin', 'scrypt:32768:8:1$Bc1xPnNtciYQhApQ$6b2d7482b30df616feb4ebda88d36f6e6ebde3ac17d6d2275765b17b76c4543f213f408852c065346dc5d760e61356ee5c01a8c18d9bca51df0ed0e4c7d6741a', 'admin@internship.com', 'admin');

-- Sample companies
INSERT IGNORE INTO companies (name, contact_person, email, phone) VALUES
('Acme Corporation', 'Sita Sharma', 'sita@acme.com', '+91-9876543210'),
('Beta Solutions', 'Ravi Kumar', 'ravi@beta.com', '+91-9123456780'),
('Tech Innovations', 'Priya Patel', 'priya@techinnov.com', '+91-9888776655');

-- Sample students
INSERT IGNORE INTO students (name, email, phone, branch) VALUES
('Aman Verma', 'aman@example.com', '+91-9999000011', 'CSE'),
('Neha Singh', 'neha@example.com', '+91-9999000022', 'IT'),
('Raj Mehta', 'raj@example.com', '+91-9999000033', 'ECE');

-- Sample internships
INSERT IGNORE INTO internships (title, company_id, start_date, end_date, stipend, seats, description) VALUES
('Web Development Intern', 1, '2025-06-01', '2025-08-31', '10000 INR/month', 5, 'Work on modern web applications using Flask and React. Learn full-stack development.'),
('Data Science Intern', 2, '2025-07-01', '2025-09-30', '15000 INR/month', 3, 'Build machine learning models and analyze data. Work with Python, TensorFlow, and Pandas.'),
('Mobile App Development', 3, '2025-06-15', '2025-09-15', '12000 INR/month', 4, 'Develop mobile applications for iOS and Android using React Native.');

-- Sample applications
INSERT IGNORE INTO applications (student_id, internship_id, status) VALUES
(1, 1, 'Applied'),
(2, 2, 'Selected'),
(3, 1, 'Applied');

-- ============================================
-- Verification Queries
-- ============================================
-- Uncomment these to verify the setup:
-- SELECT 'Database Setup Complete!' AS Status;
-- SELECT COUNT(*) AS 'Total Users' FROM users;
-- SELECT COUNT(*) AS 'Total Companies' FROM companies;
-- SELECT COUNT(*) AS 'Total Students' FROM students;
-- SELECT COUNT(*) AS 'Total Internships' FROM internships;
-- SELECT COUNT(*) AS 'Total Applications' FROM applications;

