-- Create Tables
CREATE TABLE Doctors(
    `dr_code` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `sex` BOOLEAN NOT NULL,
    `on_duty` BOOLEAN NOT NULL,
    `in_house` BOOLEAN NOT NULL,
    `attending` BOOLEAN NOT NULL,
    `phone` VARCHAR(25) NOT NULL,
    CONSTRAINT `full_name` UNIQUE (`first_name`, `last_name`)
);

CREATE TABLE Nurses(
    `rn_code` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `sex` BOOLEAN NOT NULL,
    `on_duty` BOOLEAN NOT NULL,
    `phone` VARCHAR(25) NOT NULL,
    CONSTRAINT `full_name` UNIQUE (`first_name`, `last_name`)
);

CREATE TABLE Units(
    `unit_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) UNIQUE NOT NULL,
    `dept_head` INT(11) NOT NULL,
    `phone` VARCHAR(25) NOT NULL,
    FOREIGN KEY (`dept_head`) REFERENCES Doctors(`dr_code`)
);

CREATE TABLE DoctorsUnits(
    `dr_code` INT(11) NOT NULL,
    `unit_id` INT(11) NOT NULL,
    PRIMARY KEY (`dr_code`, `unit_id`),
    FOREIGN KEY (`dr_code`) REFERENCES Doctors(`dr_code`)
        ON DELETE CASCADE,
    FOREIGN KEY (`unit_id`) REFERENCES Units(`unit_id`)
        ON DELETE CASCADE,
    CONSTRAINT `dr_unit` UNIQUE (`dr_code`, `unit_id`)
);

CREATE TABLE NursesUnits(
    `rn_code` INT(11) NOT NULL,
    `unit_id` INT(11) NOT NULL,
    PRIMARY KEY (`rn_code`, `unit_id`),
    FOREIGN KEY (`rn_code`) REFERENCES Nurses(`rn_code`)
        ON DELETE CASCADE,
    FOREIGN KEY (`unit_id`) REFERENCES Units(`unit_id`)
        ON DELETE CASCADE,
    CONSTRAINT `rn_unit` UNIQUE (`rn_code`, `unit_id`)
);

CREATE TABLE Patients(
    `pat_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `sex` BOOLEAN NOT NULL,
    `dob` DATE NOT NULL,
    `admit_date` DATE NOT NULL,
    `anticipated_discharge` DATE,
    `diagnosis` VARCHAR(255) NOT NULL,
    `code_status` VARCHAR(255) NOT NULL,
    `room` VARCHAR(10) NOT NULL,
    `rn_code` INT(11) NOT NULL,
    `dr_code` INT(11) NOT NULL,
    `unit_id` INT(11) NOT NULL,
    FOREIGN KEY (`rn_code`) REFERENCES Nurses(`rn_code`),
    FOREIGN KEY (`dr_code`) REFERENCES Doctors(`dr_code`),
    FOREIGN KEY (`unit_id`) REFERENCES Units(`unit_id`),
    CONSTRAINT `pat_info` UNIQUE (`first_name`, `last_name`, `dob`)
);


-- Insert data into Doctors

INSERT INTO Doctors (`first_name`, `last_name`, `sex`, `on_duty`, `in_house`, `attending`, `phone`)
    VALUES ("John", "Dorian", 1, 1, 1, 0, "111-111-1111"), ("Perry", "Cox", 1, 1, 1, 1, "222-222-2222"),
    ("Elliot", "Reid", 0, 1, 1, 0, "333-333-3333"), ("Christopher", "Turkleton", 1, 1, 1, 0, "444-444-4444"),
    ("Bob", "Kelso", 1, 0, 0, 1, "666-666-6666");


-- Insert data into Nurses

INSERT INTO Nurses (`first_name`, `last_name`, `sex`, `on_duty`, `phone`)
    VALUES ("Carla", "Espinosa", 0, 1, "555-555-5555"), ("Laverne", "Roberts", 0, 1, "777-777-7777"),
    ("Paul", "Flowers", 1, 0, "888-888-8888"), ("Jackie", "Peyton", 0, 0, "999-999-9999");


-- Insert data into Units

INSERT INTO Units (`name`, `dept_head`, `phone`)
    VALUES ("ER", (SELECT `dr_code` FROM Doctors WHERE `first_name` = "Bob" AND last_name = "Kelso"), "000-000-0000"),
    ("MedSurg", (SELECT `dr_code` FROM Doctors WHERE `first_name` = "Bob" AND last_name = "Kelso"), "000-000-0001"),
    ("Surgery", (SELECT `dr_code` FROM Doctors WHERE `first_name` = "Bob" AND last_name = "Kelso"), "000-000-0002");


-- Insert data into Patients

INSERT INTO Patients (`first_name`, `last_name`, `sex`, `dob`, `admit_date`, `anticipated_discharge`, `diagnosis`,
    `code_status`, `room`, `rn_code`, `dr_code`, `unit_id`)
    VALUES ("Ben", "Sullivan", 1, "1972-01-01", "2004-02-24", "2004-02-29", "Leukemia", "Full", "MS201",
    (SELECT `rn_code` FROM Nurses WHERE `first_name` = "Carla" AND `last_name` = "Espinosa"),
    (SELECT `dr_code` FROM Doctors WHERE `first_name` = "John" AND `last_name` = "Dorian"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg"));

INSERT INTO Patients (`first_name`, `last_name`, `sex`, `dob`, `admit_date`, `diagnosis`,
    `code_status`, `room`, `rn_code`, `dr_code`, `unit_id`)
    VALUES ("Mrs.", "Tanner", 0, "1938-01-01", "2001-10-16", "Lung Cancer", "DNR/DNI", "MS212",
    (SELECT `rn_code` FROM Nurses WHERE `first_name` = "Carla" AND `last_name` = "Espinosa"),
    (SELECT `dr_code` FROM Doctors WHERE `first_name` = "John" AND `last_name` = "Dorian"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg"));

INSERT INTO Patients (`first_name`, `last_name`, `sex`, `dob`, `admit_date`, `anticipated_discharge`, `diagnosis`,
    `code_status`, `room`, `rn_code`, `dr_code`, `unit_id`)
    VALUES ("Harvey", "Corman", 1, "1956-01-01", "2002-02-24", "2002-02-24", "None", "Full", "MS206",
    (SELECT `rn_code` FROM Nurses WHERE `first_name` = "Laverne" AND `last_name` = "Roberts"),
    (SELECT `dr_code` FROM Doctors WHERE `first_name` = "Perry" AND `last_name` = "Cox"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg"));

INSERT INTO Patients (`first_name`, `last_name`, `sex`, `dob`, `admit_date`, `diagnosis`,
    `code_status`, `room`, `rn_code`, `dr_code`, `unit_id`)
    VALUES ("Sam", "Thompson", 1, "1975-01-01", "2006-02-24", "Abdominal Pain", "Full", "MS213",
    (SELECT `rn_code` FROM Nurses WHERE `first_name` = "Paul" AND `last_name` = "Flowers"),
    (SELECT `dr_code` FROM Doctors WHERE `first_name` = "Elliot" AND `last_name` = "Reid"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg"));


-- Insert data into DoctorsUnits

INSERT INTO DoctorsUnits (`dr_code`, `unit_id`) VALUES (
    (SELECT `dr_code` FROM Doctors WHERE `first_name` = "John" AND `last_name` = "Dorian"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg")),
((SELECT `dr_code` FROM Doctors WHERE `first_name` = "John" AND `last_name` = "Dorian"),
    (SELECT `unit_id` FROM Units WHERE `name` = "ER")),
((SELECT `dr_code` FROM Doctors WHERE `first_name` = "Perry" AND `last_name` = "Cox"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg")),
((SELECT `dr_code` FROM Doctors WHERE `first_name` = "Elliot" AND `last_name` = "Reid"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg")),
((SELECT `dr_code` FROM Doctors WHERE `first_name` = "Christopher" AND `last_name` = "Turkleton"),
    (SELECT `unit_id` FROM Units WHERE `name` = "Surgery")),
((SELECT `dr_code` FROM Doctors WHERE `first_name` = "Christopher" AND `last_name` = "Turkleton"),
    (SELECT `unit_id` FROM Units WHERE `name` = "ER")),
((SELECT `dr_code` FROM Doctors WHERE `first_name` = "Bob" AND `last_name` = "Kelso"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg"));


-- Insert data into NursesUnits

INSERT INTO NursesUnits (`rn_code`, `unit_id`) VALUES (
    (SELECT `rn_code` FROM Nurses WHERE `first_name` = "Carla" AND `last_name` = "Espinosa"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg")),
((SELECT `rn_code` FROM Nurses WHERE `first_name` = "Laverne" AND `last_name` = "Roberts"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg")),
((SELECT `rn_code` FROM Nurses WHERE `first_name` = "Paul" AND `last_name` = "Flowers"),
    (SELECT `unit_id` FROM Units WHERE `name` = "MedSurg")),
((SELECT `rn_code` FROM Nurses WHERE `first_name` = "Jackie" AND `last_name` = "Peyton"),
    (SELECT `unit_id` FROM Units WHERE `name` = "ER")),
((SELECT `rn_code` FROM Nurses WHERE `first_name` = "Carla" AND `last_name` = "Espinosa"),
    (SELECT `unit_id` FROM Units WHERE `name` = "Surgery")),
((SELECT `rn_code` FROM Nurses WHERE `first_name` = "Carla" AND `last_name` = "Espinosa"),
    (SELECT `unit_id` FROM Units WHERE `name` = "ER"));
