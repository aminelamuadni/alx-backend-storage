-- Drop the index if it exists (in case of re-running the script)
DROP INDEX IF EXISTS idx_name_first ON names;

-- Add a generated column to store the first letter of name
ALTER TABLE
    names
ADD
    COLUMN first_letter CHAR(1) AS (SUBSTRING(name, 1, 1)) STORED;

-- Create an index on the generated column
CREATE INDEX idx_name_first ON names(first_letter);