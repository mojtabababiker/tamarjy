-- SetUp the database for the development environment
-- This script is used to create the database and the tables for the development environment
-- Create the database
CREATE DATABASE IF NOT EXISTS tamarjy_db;

-- Create the dev user if not exists
CREATE USER IF NOT EXISTS 'tamarjy_user'@'localhost' IDENTIFIED BY 'tamarjy_pwd';
GRANT ALL PRIVILEGES ON tamarjy_db.* TO 'tamarjy_user'@'localhost';
GRANT SELECT ON mysql.proc TO 'tamarjy_user'@'localhost';
