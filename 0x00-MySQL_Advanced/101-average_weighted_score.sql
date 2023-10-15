--a stored procedure
-- computes and store the average weighted score for all students.
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE user_id INT;
    DECLARE avg_weighted_score FLOAT;

    -- Initialize variables
    SET total_weighted_score = 0;
    SET total_weight = 0;

    -- Loop through users
    DECLARE done INT DEFAULT 0;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;
    user_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Calculate weighted average for each user
        SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        SELECT SUM(projects.weight) INTO total_weight
        FROM projects;

        SET avg_weighted_score = total_weighted_score / total_weight;

        -- Update user's average_score
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP;

    CLOSE cur;
END ;
//
