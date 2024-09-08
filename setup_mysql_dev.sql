-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS fit_dev_db;
CREATE USER IF NOT EXISTS 'fit_dev'@'localhost' IDENTIFIED BY 'fit_dev_pwd';
GRANT ALL PRIVILEGES ON `fit_dev_db`.* TO 'fit_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'fit_dev'@'localhost';
FLUSH PRIVILEGES;
