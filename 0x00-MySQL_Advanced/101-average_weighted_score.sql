--a stored procedure
-- computes and store the average weighted score for all students
DELIMITER // ;
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users, 
    (SELECT users.id, SUM(score * weight) / SUM(weight) AS weight_avg 
    FROM users 
    JOIN corrections as users ON users.id=users.user_id 
    JOIN projects AS project ON users.project_id=project.id
    GROUP BY users.id)
  AS weight
  SET users.average_score = weight.w_avg 
  WHERE users.id=weight.id;
END;
//
