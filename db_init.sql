-- Create database and tables for internship management
CREATE DATABASE IF NOT EXISTS internship_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE internship_db;

-- Students
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(50),
  branch VARCHAR(120),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies
CREATE TABLE IF NOT EXISTS companies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  contact_person VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Internships
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
  FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL
);

-- Applications
CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT,
  internship_id INT,
  status VARCHAR(50) DEFAULT 'Applied',
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
  FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE
);

-- Users (with roles and email for auth)
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'student',
  reset_token VARCHAR(255),
  reset_token_expires TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

INSERT INTO internships (title, company_id, start_date, end_date, stipend, seats, description) VALUES
('Web Development Intern', 1, '2025-06-01', '2025-08-31', '10000 INR/mo', 5, 'Work on Flask web apps'),
('Data Science Intern', 2, '2025-07-01', '2025-09-30', '15000 INR/mo', 3, 'Work on ML models');

INSERT INTO applications (student_id, internship_id, status) VALUES
(1,1,'Applied'),
(2,2,'Selected');
