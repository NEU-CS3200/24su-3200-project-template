DROP SCHEMA IF EXISTS petalytics;
CREATE SCHEMA petalytics;
USE petalytics;

CREATE TABLE IF NOT EXISTS agencies (
    agencyID   INTEGER      NOT NULL,
    phone      VARCHAR(255) NOT NULL,
    email      VARCHAR(255) NOT NULL,
    agencyName VARCHAR(255) NOT NULL,

    street     VARCHAR(255) NOT NULL,
    city       VARCHAR(255) NOT NULL,
    state      VARCHAR(255) NOT NULL,
    zip        INTEGER      NOT NULL,

    PRIMARY KEY (agencyID)
);

CREATE TABLE IF NOT EXISTS pets (
    petID           INTEGER PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(25) NOT NULL,
    adoption_status BOOLEAN NOT NULL DEFAULT 0,
    is_alive        BOOLEAN NOT NULL DEFAULT 1,
    species         VARCHAR(50) NOT NULL,
    breed           VARCHAR(50),
    birthday        DATE,
    age             VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS managers (
    managerID   INTEGER      NOT NULL,
    agencyID    INTEGER      NOT NULL,
    phone       VARCHAR(255) NOT NULL,
    firstName   VARCHAR(255) NOT NULL,
    lastName    VARCHAR(255) NOT NULL,
    email       VARCHAR(255) NOT NULL,

    PRIMARY KEY (managerID),
    FOREIGN KEY(agencyID)
        REFERENCES agencies(agencyID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pet_agencies (
    petID     INTEGER NOT NULL,
    agencyID  INTEGER NOT NULL,
    housingID INTEGER NOT NULL,
    entryDate DATE NOT NULL,
    exitDate  DATE,

    PRIMARY KEY (housingID),
    FOREIGN KEY (agencyID)
        REFERENCES agencies(agencyID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (petID)
        REFERENCES pets(petID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS adopters (
    adopterID INTEGER NOT NULL,
    email     VARCHAR(255) NOT NULL,
    phone     VARCHAR(255) NOT NULL,
    dob       DATE         NOT NULL,
    income    INTEGER      NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    MI        VARCHAR(1),
    lastName  VARCHAR(255) NOT NULL,
    street    VARCHAR(255) NOT NULL,
    city      VARCHAR(255) NOT NULL,
    state     VARCHAR(255) NOT NULL,
    zipcode   INTEGER      NOT NULL,

    PRIMARY KEY(adopterID)
);

CREATE TABLE IF NOT EXISTS adoptions (
    adoptionID INTEGER NOT NULL PRIMARY KEY,
    petID       INTEGER NOT NULL,
    adopterID   INTEGER NOT NULL,
    adoption_date DATE,
    adoptionStatus VARCHAR(25) NOT NULL,
    createdAt  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt  DATETIME DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_adoptions_pets FOREIGN KEY (petID) REFERENCES pets (petID),
    CONSTRAINT fk_adoptions_agency FOREIGN KEY (adopterID) REFERENCES adopters (adopterID)
);

CREATE TABLE IF NOT EXISTS medical_records (
    entryNumber INTEGER AUTO_INCREMENT,
    entry       VARCHAR(2000) NOT NULL,
    date        DATE          NOT NULL,
    petID       INTEGER       NOT NULL,
    PRIMARY KEY (entryNumber,
                petID),
    FOREIGN KEY (petID)
        REFERENCES pets(petID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);