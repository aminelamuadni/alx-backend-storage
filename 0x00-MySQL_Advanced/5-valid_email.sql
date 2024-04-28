-- Drop existing trigger if it exists to avoid conflicts
DROP TRIGGER IF EXISTS resets_valid_email;

-- Create a trigger to reset the valid_email field on email update
DELIMITER $ $ CREATE TRIGGER resets_valid_email BEFORE
UPDATE
    ON users FOR EACH ROW BEGIN IF NEW.email != OLD.email THEN
SET
    NEW.valid_email = 0;

END IF;

END $ $ DELIMITER;