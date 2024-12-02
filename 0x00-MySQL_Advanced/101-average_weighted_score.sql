DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN user_cursor;

    fetch_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE fetch_loop;
        END IF;

        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;

    CLOSE user_cursor;
END //

DELIMITER ;

