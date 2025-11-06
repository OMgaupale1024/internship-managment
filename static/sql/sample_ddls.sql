-- sample_ddls.sql
-- DDL examples for MySQL (use in MySQL Workbench)

-- 1) Create a new table for internship skills
CREATE TABLE IF NOT EXISTS internship_skills (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internship_id INT NOT NULL,
  skill VARCHAR(150) NOT NULL,
  FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE
);

-- 2) Alter table example: add a column
ALTER TABLE students ADD COLUMN roll_number VARCHAR(50);

-- 3) Drop table example (be careful)
-- DROP TABLE IF EXISTS internship_skills;
