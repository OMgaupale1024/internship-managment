-- Drop existing database and recreate with consistent collation
DROP DATABASE IF EXISTS internship_db;
CREATE DATABASE internship_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE internship_db;

-- Students
CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
  email VARCHAR(255) UNIQUE COLLATE utf8mb4_unicode_ci,
  phone VARCHAR(50) COLLATE utf8mb4_unicode_ci,
  branch VARCHAR(120) COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Companies
CREATE TABLE companies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
  contact_person VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  email VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  phone VARCHAR(50) COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Internships
CREATE TABLE internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
  company_id INT,
  start_date DATE,
  end_date DATE,
  stipend VARCHAR(100) COLLATE utf8mb4_unicode_ci,
  seats INT DEFAULT 1,
  description TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Applications
CREATE TABLE applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT,
  internship_id INT,
  status VARCHAR(50) DEFAULT 'Applied' COLLATE utf8mb4_unicode_ci,
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
  FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Users (with roles and email for auth)
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL COLLATE utf8mb4_unicode_ci,
  password_hash VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
  email VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
  role VARCHAR(50) DEFAULT 'student' COLLATE utf8mb4_unicode_ci,
  reset_token VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  reset_token_expires TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample data for testing
-- Create admin user
INSERT INTO users (username, password_hash, email, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLS9LtFgg/Qf07C', 'admin@example.com', 'admin');

-- Create company users
INSERT INTO users (username, password_hash, email, role) VALUES
('acme_corp', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLS9LtFgg/Qf07C', 'sita@acme.com', 'company'),
('beta_solutions', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLS9LtFgg/Qf07C', 'ravi@beta.com', 'company');

-- Create student users
INSERT INTO users (username, password_hash, email, role) VALUES
('aman_v', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLS9LtFgg/Qf07C', 'aman@example.com', 'student'),
('neha_s', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLS9LtFgg/Qf07C', 'neha@example.com', 'student');

-- Insert companies
INSERT INTO companies (name, contact_person, email, phone) VALUES
('Acme Corp','Sita Sharma','sita@acme.com','+91-9876543210'),
('Beta Solutions','Ravi Kumar','ravi@beta.com','+91-9123456780');

-- Insert students
INSERT INTO students (name, email, phone, branch) VALUES
('Aman Verma','aman@example.com','+91-9999000011','CSE'),
('Neha Singh','neha@example.com','+91-9999000022','IT');

-- Insert internships
INSERT INTO internships (title, company_id, start_date, end_date, stipend, seats, description) VALUES
('Web Development Intern', 1, '2025-06-01', '2025-08-31', '10000 INR/mo', 5, 'Work on Flask web apps'),
('Data Science Intern', 2, '2025-07-01', '2025-09-30', '15000 INR/mo', 3, 'Work on ML models');

-- Insert applications
INSERT INTO applications (student_id, internship_id, status) VALUES
(1,1,'Applied'),
(2,2,'Selected');