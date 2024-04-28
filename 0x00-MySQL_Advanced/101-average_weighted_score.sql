-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Set the delimiter for the procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Temporary storage for calculation results
    DECLARE done INT DEFAULT 0;
    DECLARE cur_user_id INT;
    DECLARE cur_total_weighted_score FLOAT;
    DECLARE cur_total_weight INT;

    -- Cursor to iterate through all users
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;

    -- Handler for cursor completion
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Opening cursor
    OPEN user_cursor;

    -- Iterating through all users
    user_loop: LOOP
        FETCH user_cursor INTO cur_user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Compute total weighted score for the current user
        SELECT SUM(c.score * p.weight) INTO cur_total_weighted_score
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = cur_user_id;

        -- Compute total weight for the current user
        SELECT SUM(p.weight) INTO cur_total_weight
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = cur_user_id;

        -- Update the average score
        UPDATE users
        SET average_score = IF(cur_total_weight = 0, 0, cur_total_weighted_score / cur_total_weight)
        WHERE id = cur_user_id;
    END LOOP;

    -- Closing cursor
    CLOSE user_cursor;
END$$

-- Reset the delimiter
DELIMITER ;