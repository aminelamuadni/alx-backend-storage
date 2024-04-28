-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS resets_valid_email;

-- Create a new trigger to reset the valid_email field when the email changes
DELIMITER $$
CREATE TRIGGER resets_valid_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = FALSE;
    END IF;
END$$
DELIMITER ;