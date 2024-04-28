-- Drop existing procedure to avoid conflicts
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Redefine the delimiter for complex SQL operations
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Variables to store scores and count
    DECLARE total_score DECIMAL(10, 2) DEFAULT 0.0;
    DECLARE projects_count INT DEFAULT 0;
    DECLARE calculated_average DECIMAL(10, 2) DEFAULT 0.0;

    -- Retrieve total score and count of projects for the user
    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    SELECT COUNT(*) INTO projects_count
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the average score ensuring no division by zero
    IF projects_count > 0 THEN
        SET calculated_average = total_score / projects_count;
    ELSE
        SET calculated_average = 0.0;
    END IF;

    -- Update the user's record with the computed average score
    UPDATE users
    SET average_score = calculated_average
    WHERE id = user_id;
END$$

-- Reset the delimiter to the standard semicolon
DELIMITER ;