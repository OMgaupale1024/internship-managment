-- sample_dmls.sql
-- DML examples for MySQL (use in MySQL Workbench)

-- INSERT example
INSERT INTO students (name, email, phone, branch) VALUES
('Lab Student','lab@example.com','+911112223334','CSE');

-- UPDATE example
UPDATE students SET branch='EEE' WHERE name='Lab Student';

-- DELETE example
-- DELETE FROM students WHERE name='Lab Student';

-- Aggregate/example
SELECT i.title, COUNT(a.id) AS applications
FROM internships i
LEFT JOIN applications a ON a.internship_id = i.id
GROUP BY i.id;
