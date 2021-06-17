CREATE DATABASE team_building_tool;
USE team_building_tool;
SHOW TABLES;


CREATE TABLE teachers(
    teacher_id int,
    username varchar(225),
    password varchar(225),
    PRIMARY KEY(teacher_id)
);

CREATE TABLE class(
    class_id varchar(225),
    class_name varchar(225),
    teacher_id int,
    skill1 varchar(225),
    skill2 varchar(225),
    skill3 varchar(225),
    skill4 varchar(225),
    team_size int,
    class_size int,
    PRIMARY KEY(class_id)
);

CREATE TABLE students(
    student_id int,
    class_id varchar(225),
    username varchar(225),
    password varchar(225),
    name varchar(225),
    analyst int,
    diplomat int,
    leader int, 
    explorer int,
    group_no varchar(225),
    skill1 int,
    skill2 int,
    skill3 int,
    skill4 int,
    PRIMARY KEY(student_id)
);

SELECT * FROM students;
SELECT * FROM teachers;
SELECT * FROM class;