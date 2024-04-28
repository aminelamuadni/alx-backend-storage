-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Change the delimiter for the procedure definition
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    -- Declare variables to store total scores and count of projects
    DECLARE total_score DECIMAL(10, 2);  -- Use decimal to ensure precision
    DECLARE projects_count INT;

    -- Calculate the total score for the user
    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    -- Count the number of projects for the user
    SELECT COUNT(*) INTO projects_count
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average score, ensuring division returns a decimal value
    UPDATE users
    SET average_score = IF(projects_count = 0, 0, total_score / projects_count)
    WHERE id = user_id;
END$$

-- Reset the delimiter to the standard semicolon
DELIMITER ;