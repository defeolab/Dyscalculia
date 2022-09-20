DROP TABLE IF EXISTS trial_result;
DROP TABLE IF EXISTS player;

CREATE TABLE player
(
    player_id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    username  VARCHAR(30) NULL,
    ip_address INT(11) UNSIGNED NOT NULL,

    -- acc_sharp DECIMAL(5, 2),
    -- acc_filt DECIMAL(5, 2)

    PRIMARY KEY (player_id),
    INDEX (player_id)
) ENGINE = InnoDB;

CREATE TABLE trial_result_new
(
    trial_result_id              BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    player_id                    BIGINT(20) UNSIGNED NOT NULL,
    difficulty                   DECIMAL(5, 2),
    mode                         VARCHAR(255),
    correct                      BIT NOT NULL,
    decision_time                BIGINT(20) NOT NULL,
    area_1_circle_radius         DECIMAL(5, 2) NULL,
    area_1_size_of_chicken       DECIMAL(5, 2) NULL,
    area_1_average_space_between DECIMAL(5, 2) NULL,
    area_1_number_of_chickens    INT,
    area_2_circle_radius         DECIMAL(5, 2) NULL,
    area_2_size_of_chicken       DECIMAL(5, 2) NULL,
    area_2_average_space_between DECIMAL(5, 2) NULL,
    area_2_number_of_chickens    INT,
    chicken_show_time            DECIMAL(5, 2) NULL,
    created                      DATETIME NULL,
    PRIMARY KEY (trial_result_id),

    CONSTRAINT FK_trial_result_0 FOREIGN KEY (player_id) REFERENCES player (player_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
) ENGINE = InnoDB;
