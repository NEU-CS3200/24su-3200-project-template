DROP DATABASE IF EXISTS projectTable;

CREATE DATABASE IF NOT EXISTS projectTable;

USE projectTable;

# ---------------------------------------------------------------------- #
# Tables                                                                 #
# ---------------------------------------------------------------------- #
# ---------------------------------------------------------------------- #
# Add table "Categories"                                                 #
# ---------------------------------------------------------------------- #

CREATE TABLE users (
    `FName` VARCHAR(255) NOT NULL,
    `LName` VARCHAR(255) NOT NULL,
    `Gender` ENUM('Male', 'Female', 'Other'),
    `id` INTEGER UNIQUE PRIMARY KEY,
    `age` INTEGER check (age between 18 and 120),
    `city` VARCHAR(255) NOT NULL
);

Create TABLE area (
    `id` integer UNIQUE PRIMARY KEY,
    `AveragePrice` integer NOT NULL check (AveragePrice >= 0),
    `SchoolQuality` integer NOT NULL check (SchoolQuality between 0 and 10),
    `name` varchar(255) UNIQUE Not NULL
);

Create TABLE offer (
    `Amount` integer not null ,
    `OfereeId` integer not null,
    `id` integer UNIQUE PRIMARY KEY,
    CONSTRAINT FK_Offer_Users FOREIGN KEY (OfereeId) REFERENCES users(id) ON UPDATE CASCADE
);

CREATE TABLE 'Viewed Area' (
    `UserId` integer NOT NULL,
    `AreaId` integer NOT NULL,
    CONSTRAINT FK_ViewedArea_Users FOREIGN KEY (UserId) REFERENCES users(id) ON UPDATE CASCADE on DELETE CASCADE ,
    CONSTRAINT FK_ViewedArea_Area FOREIGN KEY (AreaId) REFERENCES area(id) ON UPDATE CASCADE  on DELETE CASCADE,
    CONSTRAINT PK_ViewedArea PRIMARY KEY (`UserId`,`AreaId`)
);

Create TABLE Realtor (
    `FName` varchar(255) NOT NULL ,
    `LName` varchar(255) NOT NULL ,
    `City` varchar(255)  NOT NULL,
    `id` integer UNIQUE PRIMARY KEY
);


Create Table Listings (
    `BeingRented` boolean Not Null,
    `price` integer Not Null,
    `City` varchar(255)  NOT NULL,
    `ZipCode`varchar(255)  NOT NULL,
    `Street` varchar(255)  NOT NULL,
    `HouseNum` integer Not NULL,
    `State` varchar(255) Not Null,
    `PrevPriceData` integer Not Null,
    `CurrPriceData` integer Not Null,
    `PredictedFuturePriceData` integer NOT NULL,
    `id` integer UNIQUE PRIMARY KEY,
    `AreaId` integer NOT NULL,
    `RealtorId` integer NOT NULL,
    `Views` integer,
    CONSTRAINT FK_Listings_Area FOREIGN KEY (Areaid) REFERENCES area(id) ON UPDATE CASCADE,
    CONSTRAINT FK_Listings_Realtor FOREIGN KEY (RealtorId) REFERENCES Realtor(id) ON UPDATE CASCADE on DELETE CASCADE
);


CREATE TABLE `Listing Offer` (
    `OfferId` integer NOT NULL ,
    `ListingId` integer NOT NULL,
    CONSTRAINT FK_ListingOffer_Users FOREIGN KEY (OfferId) REFERENCES offer(id) ON UPDATE CASCADE,
    CONSTRAINT FK_ListingOffer_Area FOREIGN KEY (ListingId) REFERENCES Listings(id) ON UPDATE CASCADE,
    CONSTRAINT PK_ListingOffer PRIMARY KEY (`OfferId`,`ListingId`)
);

CREATE TABLE `Viewed Listing` (
    `UserId` integer NOT NULL,
    `ListingId` integer NOT NULL,
    CONSTRAINT FK_ViewedListing_Users FOREIGN KEY (UserId) REFERENCES users(id) ON UPDATE CASCADE on DELETE CASCADE,
    CONSTRAINT FK_ViewedListing_Listings FOREIGN KEY (ListingId) REFERENCES Listings(id) ON UPDATE CASCADE,
    CONSTRAINT PK_ViewedListing PRIMARY KEY (`UserId`,`ListingId`)
);

SELECT id, Price, CurrPriceData, PrevPriceData
FROM Listings
GROUP BY id
ORDER BY Price;

SELECT AreaId, AveragePrice, AVG((PredictedFuturePriceData-Price)/(Price * 100)) AS ROI
FROM Listings
JOIN area a ON Listings.AreaId = a.id
GROUP BY AreaId
ORDER BY ROI desc;


UPDATE Listings
SET price = 442000, PrevPriceData = 478000, CurrPriceData = 442000, PredictedFuturePriceData = 623000
WHERE id = 5;

SELECT id, price, PrevPriceData, PredictedFuturePriceData
FROM Listings
GROUP BY id
ORDER BY PredictedFuturePriceData;


SELECT AreaId, State, City, AveragePrice
FROM Listings
JOIN area a ON Listings.AreaId = a.id
GROUP BY AreaId, State, City,AveragePrice
ORDER BY AveragePrice;

SELECT City, Count(Id) AS NumInCity
FROM users
GROUP BY City
ORDER BY Count(Id) DESC;

SELECT ListingID, Count(UserId) AS NumUniqueViews
FROM `Viewed Listing`
GROUP BY ListingID
ORDER BY Count(UserId) DESC;

SELECT Age, Count(Id) AS NumUniqueUsers
FROM users
GROUP BY Age
ORDER BY Count(Id) ASC;

SELECT Gender, Count(Id) AS NumUniqueUsers
FROM users
GROUP BY Gender
ORDER BY Count(Id) ASC;


SELECT BeingRented, Count(id) As NumListings
FROM Listings
GROUP BY BeingRented;








