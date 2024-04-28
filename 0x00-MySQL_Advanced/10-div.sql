-- Drop existing function if it exists to avoid errors
DROP FUNCTION IF EXISTS SafeDiv;

-- Change the delimiter to handle complex SQL statements within the function
DELIMITER $$

CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    -- Declare a variable to hold the result
    DECLARE result FLOAT DEFAULT 0;

    -- Check if the divisor is not zero to avoid division by zero error
    IF b != 0 THEN
        SET result = a / b;
    END IF;

    -- Return the result which will be the division or 0
    RETURN result;
END$$

-- Reset the delimiter to the standard semicolon
DELIMITER ;