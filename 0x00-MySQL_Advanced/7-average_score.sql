-- Drop existing procedure if it exists to avoid conflicts
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Define delimiter to enclose the procedure
DELIMITER $$

-- Create a stored procedure to compute and store the average score for a user
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score DECIMAL(10,2) DEFAULT 0;
    DECLARE projects_count INT DEFAULT 0;
    DECLARE calculated_average DECIMAL(10,2);

    -- Calculate the total score of the user
    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    -- Count the number of projects for the user
    SELECT COUNT(*) INTO projects_count
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the average score; prevent division by zero
    SET calculated_average = IF(projects_count > 0, total_score / projects_count, 0);

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = calculated_average
    WHERE id = user_id;
END$$

-- Reset the delimiter to default
DELIMITER ;