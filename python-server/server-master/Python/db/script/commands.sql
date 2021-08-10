CREATE DATABASE dyscalculia;

USE dyscalculia;

select * from trial_result;

UPDATE trial_result SET correct = 1 WHERE (trial_result_id = 3);
UPDATE trial_result SET correct = 1 WHERE (trial_result_id = 5);
UPDATE trial_result SET correct = 1 WHERE (trial_result_id = 8);

UPDATE trial_result SET area_2_size_of_chicken = 1.0 WHERE (trial_result_id = 1);
UPDATE trial_result SET area_2_size_of_chicken = 1.6 WHERE (trial_result_id = 2);
UPDATE trial_result SET area_2_size_of_chicken = 1.5 WHERE (trial_result_id = 3);
UPDATE trial_result SET area_2_size_of_chicken = 0.6 WHERE (trial_result_id = 4);
UPDATE trial_result SET area_2_size_of_chicken = 1.7 WHERE (trial_result_id = 5);
UPDATE trial_result SET area_2_size_of_chicken = 0.7 WHERE (trial_result_id = 6);
UPDATE trial_result SET area_2_size_of_chicken = 1.3 WHERE (trial_result_id = 7);

UPDATE trial_result SET area_1_size_of_chicken = 0.9 WHERE (trial_result_id = 1);
UPDATE trial_result SET area_1_size_of_chicken = 0.2 WHERE (trial_result_id = 2);
UPDATE trial_result SET area_1_size_of_chicken = 1.7 WHERE (trial_result_id = 3);
UPDATE trial_result SET area_1_size_of_chicken = 0.1 WHERE (trial_result_id = 4);
UPDATE trial_result SET area_1_size_of_chicken = 1.1 WHERE (trial_result_id = 5);
UPDATE trial_result SET area_1_size_of_chicken = 0.3 WHERE (trial_result_id = 6);
UPDATE trial_result SET area_1_size_of_chicken = 1.9 WHERE (trial_result_id = 7);
UPDATE trial_result SET area_1_size_of_chicken = 1.5 WHERE (trial_result_id = 9);