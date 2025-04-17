DROP DATABASE IF EXISTS campusPerks_db;
CREATE DATABASE campusPerks_db;
USE campusPerks_db;

DROP TABLE IF EXISTS discount_used;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS discount;
DROP TABLE IF EXISTS club;
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS college;
DROP TABLE IF EXISTS location;

-- 1. Location table
CREATE TABLE location (
    locationId INT PRIMARY KEY,
    streetAddress VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    zipCode VARCHAR(20) NOT NULL
);

-- 2. College table
CREATE TABLE college (
    collegeName VARCHAR(100) PRIMARY KEY,
    locationId INT NOT NULL,
    noOfStores INT DEFAULT 0,
    noOfUsers INT DEFAULT 0,
    domain VARCHAR(50) NOT NULL,
    FOREIGN KEY(locationId) REFERENCES location(locationId)
);

-- 3. Store table
CREATE TABLE store (
    storeId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    locationId INT NOT NULL,
    priceRange VARCHAR(20) NOT NULL,
    noOfDiscounts INT DEFAULT 0,
    hoursOfOperations VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    phoneNo VARCHAR(50) NOT NULL,
    website VARCHAR(100),
    starRating DECIMAL(2,1),
    delivery BOOLEAN DEFAULT FALSE,
    ageRestricted BOOLEAN DEFAULT FALSE,
    totalSales DECIMAL(12,2) DEFAULT 0.00,
    noOfOrders INT DEFAULT 0,
    college VARCHAR(100) NOT NULL,
    clubId INT DEFAULT NULL,
    FOREIGN KEY (college) REFERENCES college(collegeName),
    FOREIGN KEY (locationId) REFERENCES location(locationId)
);

-- 4. Club table
CREATE TABLE club (
    clubId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    college VARCHAR(100) NOT NULL,
    storeId INT DEFAULT NULL,
    numberOfUsers INT DEFAULT 0,
    FOREIGN KEY (college) REFERENCES college(collegeName),
    FOREIGN KEY (storeId) REFERENCES store(storeId)
);

-- 5. Discount table
CREATE TABLE discount (
    discountId INT PRIMARY KEY NOT NULL,
    storeId INT NOT NULL,
    code VARCHAR(50) NOT NULL,
    percentOff INT NOT NULL,
    item VARCHAR(100),
    startDate DATETIME NOT NULL,
    endDate DATETIME,
    ageRestricted BOOLEAN DEFAULT FALSE,
    minPurchase DECIMAL(10,2),
    bdayDiscount BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (storeId) REFERENCES store(storeId)
);

-- 6. User table
CREATE TABLE user (
    username VARCHAR(50) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    password VARCHAR(128) NOT NULL,
    college VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phoneNo VARCHAR(50) NOT NULL,
    birthdate DATE NOT NULL,
    age INT,
    discountsUsed INT DEFAULT 0,
    clubId INT,
    FOREIGN KEY (college) REFERENCES college(collegeName),
    FOREIGN KEY (clubId) REFERENCES club(clubId)
);

-- 7. Admin table
CREATE TABLE admin (
    username VARCHAR(50) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phoneNo VARCHAR(50) NOT NULL,
    supportUser VARCHAR(50) DEFAULT NULL,
    supportClub INT DEFAULT NULL,
    supportStore INT DEFAULT NULL,
    FOREIGN KEY (supportUser) REFERENCES user(username),
    FOREIGN KEY (supportClub) REFERENCES club(clubId),
    FOREIGN KEY (supportStore) REFERENCES store(storeId)
);

-- 8. Discount Used (junction table)
CREATE TABLE discount_used (
    username VARCHAR(50) NOT NULL,
    discountId INT NOT NULL,
    PRIMARY KEY (username, discountId),
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (discountId) REFERENCES discount(discountId)
);

-- Indexes
CREATE INDEX idx_discount_store ON discount(storeId);
CREATE INDEX idx_discount_dates ON discount(startDate, endDate);
CREATE INDEX idx_store_college ON store(college);
CREATE INDEX idx_user_college ON user(college);
CREATE INDEX idx_discount_used ON discount_used(discountId);
CREATE INDEX idx_user_discounts ON discount_used(username);
CREATE UNIQUE INDEX idx_store_name_location ON store(name, locationId);
CREATE UNIQUE INDEX idx_discount_code ON discount(storeId, code);