DROP SCHEMA IF EXISTS getawayGuru;
CREATE SCHEMA getawayGuru;
USE getawayGuru;

CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                      ON UPDATE CURRENT_TIMESTAMP,
    email VARCHAR(255) UNIQUE NOT NULL,
    active BOOL DEFAULT TRUE NOT NULL,
    address VARCHAR(255),
);

CREATE TABLE IF NOT EXISTS trip(
    id INT PRIMARY KEY NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE DEFAULT CURRENT_DATE,
    group_size INT,
    name varchar(255),
    restuarant_budget INT NOT NULL,
    transportation_budget INT NOT NULL,
    hotel_budget INT NOT NULL,
    attraction_budget INT NOT NULL,
    city_id INT NOT NULL,
    FOREIGN KEY (city_id)
        REFERENCES city(id)
        ON UPDATE cascade
        ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS
