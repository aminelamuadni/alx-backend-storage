-- Create a table 'users' with a restricted country enumeration
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
    CONSTRAINT uc_Email UNIQUE (email)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;