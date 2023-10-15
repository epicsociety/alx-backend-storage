-- SQL script that creates a function
-- divides (and returns) the first by the second number
DELIMITER // ;
CREATE FUNCTION SafeDiv(
	a INT,
	b INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
	DECLARE result FLOAT;
	IF b = 0 THEN
		RETURN 0;
  END IF;
  SET result = a / b;
  RETURN result;
END;
//
