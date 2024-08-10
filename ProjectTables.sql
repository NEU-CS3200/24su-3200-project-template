DROP DATABASE IF EXISTS projectTable;

CREATE DATABASE IF NOT EXISTS projectTable;

USE projectTable;

# ---------------------------------------------------------------------- #
# Tables                                                                 #
# ---------------------------------------------------------------------- #
# ---------------------------------------------------------------------- #
# Add table "Categories"                                                 #
# ---------------------------------------------------------------------- #

CREATE TABLE `users` (
    `FName` VARCHAR(255) NOT NULL,
    `LName` VARCHAR(255) NOT NULL,
    `Gender` ENUM('Male', 'Female', 'Other'),
    `id` INTEGER UNIQUE PRIMARY KEY,
    `age` INTEGER check (age between 18 and 120),
    `city` VARCHAR(255) NOT NULL
);

Create TABLE `area` (
    `id` integer UNIQUE PRIMARY KEY,
    `AveragePrice` integer NOT NULL check (AveragePrice >= 0),
    `SchoolQuality` integer NOT NULL check (SchoolQuality between 0 and 10),
    `name` varchar(255) UNIQUE Not NULL
);

Create TABLE `offer` (
    `Amount` integer not null ,
    `OfereeId` integer not null,
    `id` integer UNIQUE PRIMARY KEY,
    CONSTRAINT FK_Offer_Users FOREIGN KEY (OfereeId) REFERENCES users(id) ON UPDATE CASCADE
);

CREATE TABLE `Viewed Area` (
    `UserId` integer NOT NULL,
    `AreaId` integer NOT NULL,
    CONSTRAINT FK_ViewedArea_Users FOREIGN KEY (UserId) REFERENCES users(id) ON UPDATE CASCADE on DELETE CASCADE ,
    CONSTRAINT FK_ViewedArea_Area FOREIGN KEY (AreaId) REFERENCES area(id) ON UPDATE CASCADE  on DELETE CASCADE,
    CONSTRAINT PK_ViewedArea PRIMARY KEY (`UserId`,`AreaId`)
);

Create TABLE `Realtor` (
    `FName` varchar(255) NOT NULL ,
    `LName` varchar(255) NOT NULL ,
    `City` varchar(255)  NOT NULL,
    `id` integer UNIQUE PRIMARY KEY
);


Create Table `Listings` (
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


INSERT INTO `users` (`FName`, `LName`, `Gender`, `id`, `age`, `city`) VALUES
('John', 'Doe', 'Male', 1, 25, 'New York'),
('Jane', 'Smith', 'Female', 2, 30, 'Los Angeles'),
('Sam', 'Johnson', 'Other', 3, 22, 'Chicago'),
('Alice', 'Williams', 'Female', 4, 28, 'Houston'),
('Bob', 'Brown', 'Male', 5, 35, 'Phoenix');

INSERT INTO `area` (`id`, `AveragePrice`, `SchoolQuality`,`Name`) VALUES
(1, 250000, 8,'West Coast'),
(2, 300000, 7, 'NorthEast'),
(3, 180000, 9, 'Midwest'),
(4, 450000, 6,'South'),
(5, 220000, 8,'SouthWest');

INSERT INTO `offer` (`Amount`, `OfereeId`, `id`) VALUES
(200000, 1, 1),
(310000, 2, 2),
(185000, 3, 3),
(400000, 4, 4),
(210000, 5, 5);

INSERT INTO `Viewed Area` (`UserId`, `AreaId`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);


INSERT INTO `Realtor` (`FName`, `LName`,`City`, `id`) VALUES
('Michael', 'Los Angeles','Clark', 1),
('Linda', 'New York' ,'Wright', 2),
('Robert','Chicago','Taylor', 3),
('Patricia', 'Chicago','Anderson', 4),
('David', 'Houston','Moore', 5);

INSERT INTO `Listings` (`BeingRented`, `price`, `City`, `ZipCode`, `Street`, `HouseNum`, `State`, `PrevPriceData`, `CurrPriceData`, `PredictedFuturePriceData`, `id`, `AreaId`, `RealtorId`, `Views`) VALUES
(TRUE, 300000, 'Los Angeles', '90001', 'Palm St', 123, 'CA', 280000, 300000, 320000, 1, 1, 1, 15),
(FALSE, 450000, 'New York', '10001', 'Oak St', 234, 'NY', 400000, 450000, 470000, 2, 2, 2, 12),
(TRUE, 235000, 'Chicago', '60007', 'Maple Ave', 345, 'IL', 220000, 235000, 240000, 3, 3, 3, 9),
(FALSE, 520000, 'Houston', '77001', 'Elm Rd', 456, 'TX', 510000, 520000, 540000, 4, 4, 4, 8);

INSERT INTO `Listing Offer` (`OfferId`, `ListingId`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO `Viewed Listing` (`UserId`, `ListingId`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

SELECT id, Price, CurrPriceData, PrevPriceData
FROM Listings
GROUP BY id
ORDER BY Price;

SELECT AreaId, AveragePrice, AVG((PredictedFuturePriceData-Price)/(Price * 100)) AS ROI
FROM Listings
JOIN area a ON Listings.AreaId = a.id
GROUP BY AreaId
ORDER BY ROI desc;


INSERT INTO `Listings` (`BeingRented`, `price`, `City`, `ZipCode`, `Street`, `HouseNum`, `State`, `PrevPriceData`, `CurrPriceData`, `PredictedFuturePriceData`, `id`, `AreaId`, `RealtorId`, `Views`) VALUES
(TRUE, 290000, 'Phoenix', '85001', 'Cedar Blvd', 567, 'AZ', 270000, 290000, 310000, 5, 5, 5, 14);


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








