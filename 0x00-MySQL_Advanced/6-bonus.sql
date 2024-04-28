-- Drop existing procedure if it exists to avoid conflicts
DROP PROCEDURE IF EXISTS AddBonus;

-- Define delimiter to enclose the procedure
DELIMITER $$

-- Create a stored procedure to add or update project scores
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;

    -- Check if the project already exists and retrieve its ID
    SELECT id INTO project_id FROM projects WHERE name = project_name LIMIT 1;

    -- If the project does not exist, create it and get the new ID
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the correction with the appropriate project ID
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END$$

-- Reset the delimiter to default
DELIMITER ;