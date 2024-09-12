-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS fit_dev_db;
CREATE USER IF NOT EXISTS 'fit_dev'@'localhost' IDENTIFIED BY 'fit_dev_pwd';
GRANT ALL PRIVILEGES ON `fit_dev_db`.* TO 'fit_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'fit_dev'@'localhost';
FLUSH PRIVILEGES;

-- Add Excesizes
USE fit_dev_db;
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('f0fa151c-8a1e-41a2-b0e2-df2231e92e8b', 'leg', 'Squat', 'A basic lower-body exercise to strengthen the legs.', 60, 4);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('0e779ce8-453c-46b4-acaf-09c5ab0142d5', 'leg', 'Lunge', 'A lower-body exercise that targets the quads and glutes.', 60, 3);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('c20824c0-fc21-47f1-9508-4283be03816c', 'leg', 'Leg Press', 'A machine-based exercise for building leg strength.', 90, 4);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('8efe5627-5059-41f9-9459-968168733703', 'chest', 'Bench Press', 'A chest exercise to build upper body strength.', 90, 4);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('1f514380-1df9-452c-823f-4ec9b3105cc5', 'chest', 'Chest Fly', 'An isolation exercise for the chest muscles.', 60, 3);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('a55c3a29-4fbe-4305-ae6f-16e4964b76ab', 'chest', 'Push Up', 'A bodyweight exercise for chest and upper body.', 45, 4);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('2a876e3d-80a7-4fb3-ac44-803d395b11fa', 'shoulders', 'Overhead Press', 'A shoulder exercise to build strength.', 90, 4);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('c27cb6c8-28d5-4525-b1d8-345f499ec332', 'shoulders', 'Lateral Raise', 'An isolation exercise for shoulder muscles.', 60, 3);
INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('0cdac027-1daa-49f3-98c7-4b1d2dc15568', 'shoulders', 'Front Raise', 'A front deltoid isolation exercise.', 60, 3);