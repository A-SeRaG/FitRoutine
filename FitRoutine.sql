CREATE DATABASE  IF NOT EXISTS FitRoutine;
CREATE TABLE User
(
    user_id INT not null auto,
   first_name VARCHAR(50 ) not NULL,
   last_name VARCHAR(50)not null,
    date_of_birth date not null,
    age INT not null,
    phone INT not null,
    usr_country VARCHAR(256) not null,
    gender BIT not null,
    usr_weight INT not null, 
    usr_height INT not null,
    primary key(user_id)
    
);
CREATE TABLE IF NOT EXISTS exercise
(
    exercise_id INT NOT NULL auto,
    excercise_name VARCHAR(8) not null,
    exercise_description VARCHAR(20) not null,
    target_muscle VARCHAR(128) not null,
    exercise_sets INT not null,
    reps INT not null,
    rest_period INT not null,
    IsInjury BIT not null,
    primary key(exercise_id)

);
CREATE TABLE IF NOT EXISTS review
(
    exercise_id INT not NULL auto,
    user_id INT not NULL,
    stars INT NOT NULL,
    text VARCHAR(256) not null,
    Foreign key(exercise_id)
);

