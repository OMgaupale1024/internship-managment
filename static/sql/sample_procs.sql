-- sample_procs.sql
-- Stored procedure examples for MySQL (MySQL uses stored procedures; PL/SQL is Oracle-specific)

DELIMITER $$
CREATE PROCEDURE sp_count_applications_for_internship(IN iid INT)
BEGIN
  SELECT i.title, COUNT(a.id) AS applications
  FROM internships i
  LEFT JOIN applications a ON a.internship_id = i.id
  WHERE i.id = iid
  GROUP BY i.id;
END$$
DELIMITER ;

-- Call example:
-- CALL sp_count_applications_for_internship(1);
