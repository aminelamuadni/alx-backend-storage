-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Change the delimiter for the procedure definition
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE total_score INT DEFAULT 0;
    DECLARE projects_count INT DEFAULT 0;

    -- Calculate the total score for the user
    SELECT SUM(score)
        INTO total_score
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Count the number of projects for the user
    SELECT COUNT(*)
        INTO projects_count
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Update the user's average score, ensuring division returns a decimal value
    UPDATE users
        SET users.average_score = IF(projects_count = 0, 0, total_score / projects_count)
        WHERE users.id = user_id;
END $$

-- Reset the delimiter to the standard semicolon
DELIMITER ;