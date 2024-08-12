-- Create database

DROP DATABASE IF EXISTS foond;
CREATE DATABASE foond;

USE foond;

-- Create tables

CREATE TABLE Customer
(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    longitude     FLOAT,
    latitude      FLOAT,
    email         VARCHAR(255) UNIQUE NOT NULL,
    firstName     VARCHAR(255)        NOT NULL,
    middleInitial CHAR(1),
    lastName      VARCHAR(255)        NOT NULL
);

CREATE TABLE Diet_Category
(
    id             INT PRIMARY KEY AUTO_INCREMENT,
    name           VARCHAR(255) UNIQUE NOT NULL,
    description    VARCHAR(255)        NOT NULL DEFAULT '',
    parentCategory INT,
    FOREIGN KEY (parentCategory) REFERENCES Diet_Category (id)
);

CREATE TABLE Cust_Diet
(
    custId INT,
    dietId INT,
    PRIMARY KEY (custId, dietId),
    FOREIGN KEY (custId) REFERENCES Customer (id),
    FOREIGN KEY (dietId) REFERENCES Diet_Category (id)
);

CREATE TABLE Formality
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        varchar(255) UNIQUE NOT NULL,
    description varchar(255)        NOT NULL DEFAULT ''
);

CREATE TABLE Price
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    rating      VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(2000)      NOT NULL DEFAULT ''
);

CREATE TABLE Cuisine
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255)        NOT NULL DEFAULT ''
);

CREATE TABLE Restaurant
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    email       VARCHAR(255) NOT NULL,
    phone       VARCHAR(255) NOT NULL,
    priceId     INT,
    formalityId INT,
    UNIQUE INDEX uq_id (id),
    CONSTRAINT fk_rest_pri
        FOREIGN KEY (priceId) REFERENCES Price (id)
            ON UPDATE cascade,
    CONSTRAINT fk_rest_form
        FOREIGN KEY (formalityId) REFERENCES Formality (id)
            ON UPDATE cascade
);

CREATE TABLE Rest_Diet
(
    restId INT,
    dietId INT,
    PRIMARY KEY (restId, dietId),
    FOREIGN KEY (restId) REFERENCES Restaurant (id),
    FOREIGN KEY (dietId) REFERENCES Diet_Category (id)
);

CREATE TABLE Location
(
    restId    INT,
    latitude  FLOAT,
    longitude FLOAT,
    PRIMARY KEY (restId, latitude, longitude),
    CONSTRAINT fk_loc
        FOREIGN KEY (restId) REFERENCES Restaurant (id)
);

CREATE TABLE Operating_Hours
(
    restId    INT,
    dayOfWeek INT,
    startTime TIME,
    endTime   TIME,
    PRIMARY KEY (restId, dayOfWeek),
    CONSTRAINT fk_op
        FOREIGN KEY (restId) REFERENCES Restaurant (id)
);

CREATE TABLE Rest_Cuisine
(
    restId    INT,
    cuisineId INT,
    PRIMARY KEY (restId, cuisineId),
    FOREIGN KEY (restId) REFERENCES Restaurant (id),
    FOREIGN KEY (cuisineId) REFERENCES Cuisine (id)
);

CREATE TABLE Cust_Cuisine
(
    custId    INT,
    cuisineId INT,
    PRIMARY KEY (custId, cuisineId),
    FOREIGN KEY (custId) REFERENCES Customer (id),
    FOREIGN KEY (cuisineId) REFERENCES Cuisine (id)
);

CREATE TABLE Cust_Price
(
    custId  INT,
    priceId INT,
    PRIMARY KEY (custId, priceId),
    FOREIGN KEY (custId) REFERENCES Customer (id),
    FOREIGN KEY (priceId) REFERENCES Price (id)
);

CREATE TABLE Dining_Group
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        varchar(255) NOT NULL,
    description varchar(255) NOT NULL DEFAULT ''
);

CREATE TABLE Recommendation
(
    seqNum      INT,
    custId      INT,
    restId      INT          NOT NULL,
    explanation varchar(255) NOT NULL DEFAULT '',
    accepted    BOOL         NOT NULL DEFAULT FALSE,
    dateGiven   DATETIME              DEFAULT CURRENT_TIMESTAMP,
    groupId     INT,
    PRIMARY KEY (custId, seqNum),
    FOREIGN KEY (restId) REFERENCES Restaurant (id),
    FOREIGN KEY (custId) REFERENCES Customer (id),
    FOREIGN KEY (groupId) REFERENCES Dining_Group (id)
);

CREATE TABLE Cust_Formality
(
    custId      INT,
    formalityId INT,
    PRIMARY KEY (custId, formalityId),
    FOREIGN KEY (custId) REFERENCES Customer (id),
    FOREIGN KEY (formalityId) REFERENCES Formality (id)
);

CREATE TABLE Recommendation_Review
(
    seqNum         INT,
    custId         INT,
    dateGiven      DATETIME DEFAULT CURRENT_TIMESTAMP,
    comment        varchar(255),
    dietScore      INT,
    priceScore     INT,
    cuisineScore   INT,
    formalityScore INT,
    locationScore  INT,
    PRIMARY KEY (seqNum, custId),
    FOREIGN KEY (custId, seqNum) REFERENCES Recommendation (custId, seqNum)
);

CREATE TABLE Cust_Group
(
    custId  INT,
    groupId INT,
    PRIMARY KEY (custId, groupId),
    FOREIGN KEY (custId) REFERENCES Customer (id),
    FOREIGN KEY (groupId) REFERENCES Dining_Group (id)
);
