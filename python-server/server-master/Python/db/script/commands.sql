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

DROP Table PDEP_player_info;

CREATE TABLE PDEP_player_info (
    player_id bigint(20) unsigned,
    
    alpha decimal(5,2),
    sigma decimal(5, 4),
    
    PRIMARY KEY (player_id)
);

DROP Table PDEP_probability_history;

CREATE TABLE PDEP_probability_history (
    player_id bigint(20) unsigned,
    
    error_probability decimal(5, 4),
    perceived_difficulty decimal(5,4),
    
    PRIMARY KEY (player_id)
);

DROP Table PDEP_trial_result;

CREATE TABLE PDEP_trial_result (
	trial_result_id bigint(20) unsigned auto_increment,
    player_id bigint(20) unsigned,
    correct bit(1),
    prediction bit(1),
    decision_time bigint(20),
    
    target_error_probability DECIMAL(3, 2),
    target_perceived_difficulty DECIMAL(3, 2),

    estimated_alpha DECIMAL(5,2),
    estimated_sigma DECIMAL(5,4),

    ND decimal(5,4),
    NND decimal(5,4),
    id_in_lookup_table bigint(20) unsigned,
    
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




