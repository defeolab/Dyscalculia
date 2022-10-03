CREATE DATABASE dyscalculia;

USE dyscalculia;

select * from trial_result;

select * from trial_result_new;
drop table trial_result_new;

CREATE TABLE trial_result_new (
    trial_result_id bigint(20) unsigned auto_increment,
    player_id bigint(20) unsigned,
    correct bit(1),
    decision_time bigint(20),
    difficulty decimal (5,2),
    trial_mode VARCHAR(32),
    area_1_circle_radius decimal (5,2),
    area_1_size_of_chicken decimal (5,2),
    area_1_average_space_between decimal (5,2),
    area_1_number_of_chickens int(11),
    area_2_circle_radius decimal (5,2),
    area_2_size_of_chicken decimal (5,2),
    area_2_average_space_between decimal (5,2),
    area_2_number_of_chickens int(11),
    chicken_show_time decimal(5,2),
    created datetime,
    PRIMARY KEY (trial_result_id)
);

CREATE TABLE player_info (
    player_id bigint(20) unsigned,
    
    filtering_total bigint(20) unsigned,
    filtering_correct bigint(20) unsigned,
    filtering_diff decimal (5,2),
    filtering_total_time bigint(20),
    
    sharpening_total bigint(20) unsigned,
    sharpening_correct bigint(20) unsigned,
    sharpening_diff decimal (5,2),
    sharpening_total_time bigint(20),
    
    PRIMARY KEY (player_id)
);