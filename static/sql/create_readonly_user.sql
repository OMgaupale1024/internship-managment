-- Create a read-only user for demonstration (run as root or a user with privileges)
-- Replace 'readonly_user' and 'strong_password' with your desired values.

CREATE USER IF NOT EXISTS 'readonly_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT ON internship_db.* TO 'readonly_user'@'localhost';
FLUSH PRIVILEGES;

-- To test from MySQL Workbench, connect with the new user and try SELECT queries.
