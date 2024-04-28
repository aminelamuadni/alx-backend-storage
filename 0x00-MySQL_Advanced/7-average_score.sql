-- Drop existing procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Set the delimiter to allow complex statement inside the procedure
DELIMITER $$

-- Create a new procedure to calculate the average score
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Variables to hold the scores sum and count of corrections
    DECLARE total_score DECIMAL(10, 2);
    DECLARE score_count INT;

    -- Calculate the sum of scores for the given user
    SELECT SUM(score) INTO total_score FROM corrections WHERE user_id = user_id;

    -- Count the number of scores entries for the given user
    SELECT COUNT(*) INTO score_count FROM corrections WHERE user_id = user_id;

    -- Update the average score in the users table
    -- Check if there are any scores to avoid division by zero
    IF score_count > 0 THEN
        UPDATE users SET average_score = total_score / score_count WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END$$

-- Reset the delimiter
DELIMITER ;