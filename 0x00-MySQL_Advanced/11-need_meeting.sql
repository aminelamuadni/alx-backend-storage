-- Drop the view if it already exists to avoid errors on recreation
DROP VIEW IF EXISTS need_meeting;

-- Create the view `need_meeting` to identify students needing a meeting
CREATE VIEW need_meeting AS
SELECT
    name
FROM
    students
WHERE
    score < 80
    AND (
        last_meeting IS NULL
        OR last_meeting < SUBDATE(CURRENT_DATE(), INTERVAL 1 MONTH)
    );