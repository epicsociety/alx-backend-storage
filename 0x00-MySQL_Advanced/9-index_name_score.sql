-- SQL script that creates an index on the table names
-- on the first letter of name and the score
CREATE INDEX idx_name_first_score on names(name(1), score)
