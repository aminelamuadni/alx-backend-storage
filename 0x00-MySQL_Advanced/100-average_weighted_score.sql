-- Drop existing procedure if it exists to avoid errors on recreation
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Change the delimiter to handle complex SQL statements within the function
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    -- Variables to hold the sum of weighted scores and the sum of weights
    DECLARE total_weighted_score FLOAT DEFAULT 0.0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the total weighted score for the user
    SELECT SUM(corrections.score * projects.weight)
        INTO total_weighted_score
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    -- Calculate the total weight for the user
    SELECT SUM(projects.weight)
        INTO total_weight
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    -- Update the user's average score
    -- Check if the total weight is zero to avoid division by zero
    IF total_weight = 0 THEN
        UPDATE users SET average_score = 0 WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = total_weighted_score / total_weight WHERE id = user_id;
    END IF;
END$$

-- Reset the delimiter to the standard semicolon
DELIMITER ;