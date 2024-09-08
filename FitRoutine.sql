CREATE DATABASE FitRoutine;
CREATE TABLE User
(
    user_id INT not null,
   first_name VARCHAR(50 not null),
   last_name VARCHAR(50)not null,
    date_of_birth date,
    age INT,
    phone INT,
    usr_country VARCHAR(256),
    gender BIT,
    usr_weight INT, 
    usr_height INT,
        primary key(user_id)
    
);
CREATE TABLE IF NOT EXISTS exercise
(
    exercise_id INT NOT NULL,
    excercise_name VARCHAR(8),
    exercise_description VARCHAR(20),
    target_muscle VARCHAR(128),
    exercise_sets INT,
    reps INT,
    rest_period INT,
    IsInjury BIT,
    primary key(exercise_id)

);

