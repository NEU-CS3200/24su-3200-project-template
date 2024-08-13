DROP DATABASE IF EXISTS homeFinderTables;

CREATE DATABASE IF NOT EXISTS homeFinderTables;

USE homeFinderTables;


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


INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Matias', 'MacShane', 'other', '74', 'Jacksonville', '3');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Morris', 'Housegoe', 'other', '54', 'Charlestown', '4');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Maribelle', 'Prettejohns', 'other', '94', 'Kawaguchi', '1');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Madelene', 'ODonnell', 'other', '59', 'Tagasilay', '2');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Evangelin', 'Eagan', 'other', '58', 'Cigarogol', '5');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Dosi', 'Sherebrooke', 'female', '90', 'Lubasz', '6');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Jose', 'Ziem', 'other', '68', 'Slobodka', '7');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Karyl', 'Brumby', 'female', '87', 'Bebedouro', '8');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Odey', 'Boeter', 'other', '21', 'Boston', '9');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Anatola', 'Cardwell', 'other', '42', 'Dhuusamarreeb', '10');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Ginger', 'Huskinson', 'other', '92', 'Pajapita', '11');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Hyman', 'Renner', 'male', '23', 'Stavanger', '12');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Barbee', 'Fallowes', 'female', '18', 'Jenamas', '13');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Madlin', 'Dulanty', 'other', '85', 'Bromma', '14');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Ingrim', 'Kuhnel', 'female', '18', 'Yepocapa', '15');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Obediah', 'Brinicombe', 'other', '84', 'Huangguan', '16');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Jemimah', 'Jaspar', 'other', '92', 'Baruta', '17');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Jewelle', 'Bernardos', 'male', '32', 'Tunduma', '18');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Sibel', 'Draisey', 'other', '100', 'Medway', '19');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Yorke', 'Broxap', 'female', '58', 'Sohag', '20');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Pierette', 'Tellenbroker', 'female', '62', 'Bilshivtsi', '21');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Allayne', 'Jamison', 'female', '25', 'Athabasca', '22');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Ingaborg', 'Densell', 'other', '66', 'Ruteng', '23');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Gerek', 'Coslett', 'other', '52', 'Xinzhaiping', '24');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Bernita', 'Harford', 'other', '45', 'New York', '25');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Marcela', 'Bonson', 'other', '23', 'Fenghuang', '26');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Kirbee', 'Sharer', 'male', '44', 'San Fransisco', '27');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Lorelle', 'Guilloux', 'female', '79', 'Meghrashen', '28');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Heida', 'Dower', 'male', '92', 'Ciudad Arce', '29');
INSERT INTO `users` (fname, lname, gender, age, city, id) VALUES ('Cati', 'Cuttler', 'other', '53', 'Orlando', '30');

INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Dougie', 'Boggas', 'Xinglongquan', '1');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Freddi', 'Slora', 'Boston', '2');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Earvin', 'Wakeling', 'Jalal-Abad', '3');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Raviv', 'McMains', 'Tawali', '4');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Wilmer', 'Fee', 'Qingshui', '5');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Ezra', 'Olivo', 'Xinzhan', '6');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Agnella', 'Langrish', 'Playas', '7');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Ingunna', 'Dibben', 'Jiangchuanlu', '8');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Ardis', 'Marrion', 'Gaborone', '9');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Andris', 'Germain', 'Sarae', '10');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Natale', 'Devennie', 'Oenam', '11');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Dougy', 'Gambell', 'Gaotan', '12');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Ted', 'Lockier', 'New York', '13');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Oliviero', 'OShesnan', 'Lafia', '14');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Rhodie', 'Burnsyde', 'Billings', '15');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Frank', 'Rosenshine', 'Heshe', '16');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Teressa', 'Videler', 'Huocheng', '17');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Brittan', 'Berkery', 'Lamarosa', '18');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Jennica', 'Biskup', 'Zhavoronki', '19');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Parsifal', 'Rowth', 'Venlo', '20');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Chick', 'Tremblay', 'Chutove', '21');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Wilmar', 'Jezzard', 'Kertasari', '22');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Barbey', 'Barhems', 'Toledo', '23');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Elston', 'Staresmeare', 'Shouzhan', '24');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Daisey', 'Kilshall', 'Kangar', '25');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Gill', 'Sergean', 'Indianapolis', '26');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Magdalena', 'Longmaid', 'Karata', '27');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Lee', 'Curtiss', 'Miami', '28');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Verge', 'Neasham', 'Caballococha', '29');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Carlotta', 'Blofeld', 'Kostel', '30');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Adena', 'Strettell', 'Chalu', '31');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Robinet', 'Twelvetree', 'Bueng Kan', '32');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Jerald', 'Kernar', 'Zarqa', '33');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Dannie', 'Gannan', 'Linshanhe', '34');
INSERT INTO `Realtor` (FName, LName, City, id) VALUES ('Marshal', 'Trenfield', 'Xiaoguwei', '35');

INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('427980', '3', 'Greater Boston', '1');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2564151', '9', 'Bay Area', '2');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2969405', '4', 'Pacific Northwest', '3');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2873671', '6', 'Midwest', '4');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2977237', '4', 'Sunbelt', '5');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('141662', '2', 'Northeast', '6');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2686330', '1', 'Southwest', '7');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2238551', '2', 'Rocky Mountains', '8');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('2819856', '4', 'Great Plains', '9');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('339122', '10', 'Deep South', '10');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('555872', '1', 'Mid-Atlantic', '11');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('826759', '8', 'Gulf Coast', '12');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('1728771', '8', 'Appalachia', '13');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('893798', '6', 'Great Lakes', '14');
INSERT INTO `area` (AveragePrice, SchoolQuality, name, id) VALUES ('103220', '10', 'South Central', '15');

INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Las Vegas', '32223', 'Maple Street', '3', 'Arizona','2014873', '3426174', '2004330', '10', '35', '1');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Boise', '54321', 'Oak Avenue', '82541', 'Nebraska','2000231', '1716677', '184757', '2', '28', '2');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Los Angeles', '98765', 'Pine Road', '9042', 'Illinois','1518364', '236951', '3690722', '14', '16', '3');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Portland', '67890', 'Cedar Lane', '69861', 'Mississippi','895446', '2603551', '2750268', '15', '22', '4');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Austin', '45678', 'Elm Boulevard', '039', 'Maryland','936421', '2006015', '2385292', '1', '12', '5');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Raleigh', '23456', 'Willow Drive', '1846', 'Kansas','1839586', '213740', '2669041', '10', '19', '6');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Jacksonville', '87654', 'Birch Court', '8', 'Hawaii','344493', '1296716', '1014173', '3', '26', '7');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Austin', '34567', 'Aspen Way', '63', 'Colorado','1661034', '3300253', '3871273', '15', '3', '8');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Memphis', '78901', 'Hickory Circle', '826', 'Illinois','1202537', '3924765', '1594257', '10', '1', '9');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Memphis', '56789', 'Spruce Place', '31', 'Texas','560107', '3814535', '1356393', '15', '10', '10');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Madison', '21098', 'Magnolia Lane', '53', 'Texas','2573658', '1785720', '2742827', '11', '8', '11');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Springfield', '87654', 'Sycamore Street', '180', 'Georgia','699134', '3757825', '449473', '6', '11', '12');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Springfield', '54321', 'Juniper Avenue', '5', 'Minnesota','1836118', '2640727', '1766066', '11', '35', '13');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Seattle', '10987', 'Cypress Road', '5', 'New York','3170738', '3308827', '2009891', '15', '6', '14');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Houston', '76543', 'Poplar Lane', '99', 'Texas','1490145', '1577441', '1441625', '13', '19', '15');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Houston', '32109', 'Beech Drive', '29', 'Minnesota','3303589', '609773', '546724', '2', '11', '16');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Fargo', '65432', 'Alder Boulevard', '0903', 'Delaware','622815', '2359289', '1292834', '8', '9', '17');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Chicago', '89012', 'Chestnut Road', '37', 'Arkansas','82877', '256540', '3259431', '5', '35', '18');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Austin', '43210', 'Fir Avenue', '61', 'Tennessee','2396903', '95300', '2285426', '10', '2', '19');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Memphis', '67890', 'Linden Court', '1', 'Pennsylvania','449205', '111757', '293296', '3', '4', '20');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Jacksonville', '21098', 'Mulberry Way', '0', 'Indiana','1730296', '1168866', '1207935', '15', '9', '21');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Seattle', '87654', 'Walnut Circle', '71913', 'Georgia','3633016', '3298649', '171298', '12', '23', '22');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Albany', '54321', 'Cherry Place', '1', 'Michigan','2134649', '251159', '2718894', '9', '5', '23');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Cheyenne', '10987', 'Sassafras Lane', '417', 'Florida','3554068', '410096', '264076', '10', '32', '24');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Raleigh', '76543', 'Hemlock Street', '18', 'Washington','3188695', '3929224', '2490787', '11', '33', '25');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Miami', '32109', 'Locust Avenue', '8866', 'Indiana','1987084', '3953817', '844864', '12', '11', '26');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Austin', '65432', 'Ash Road', '40', 'Nebraska','640244', '3212852', '2244707', '9', '17', '27');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Albany', '89012', 'Dogwood Lane', '85', 'Illinois','2800050', '2600453', '3793009', '3', '29', '28');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Memphis', '43210', 'Palm Drive', '416', 'California','3280334', '1798586', '3700502', '7', '33', '29');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Los Angeles', '67890', 'Bamboo Boulevard', '64', 'Louisiana','2297559', '161551', '2735324', '15', '12', '30');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Birmingham', '21098', 'Banyan Way', '95411', 'Georgia','1267084', '3510009', '3467351', '2', '28', '31');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Denver', '87654', 'Bougainvillea Circle', '3913', 'District of Columbia','3199800', '162270', '1406111', '11', '15', '32');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Boston', '54321', 'Camellia Place', '515', 'Pennsylvania','1380777', '2654587', '3053725', '9', '16', '33');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Birmingham', '10987', 'Dahlia Street', '17', 'Ohio','2482753', '2741976', '2233915', '5', '20', '34');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Cheyenne', '76543', 'Eucalyptus Avenue', '34', 'Florida','853589', '2472743', '3879072', '14', '24', '35');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Chicago', '32109', 'Fuchsia Road', '3', 'Illinois','1064866', '543412', '3254828', '10', '13', '36');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Atlanta', '65432', 'Gardenia Lane', '6', 'Texas','505550', '808283', '2719865', '12', '14', '37');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Albany', '89012', 'Hyacinth Boulevard', '660', 'Wisconsin','2814123', '1759352', '3014650', '9', '9', '38');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Salem', '43210', 'Iris Drive', '3', 'California','2125589', '3992280', '2843297', '1', '7', '39');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Houston', '67890', 'Jasmine Court', '9', 'Missouri','845041', '3816894', '398789', '15', '6', '40');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Madison', '21098', 'Kale Road', '2544', 'Texas','2751294', '153033', '2362231', '8', '22', '41');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Salem', '87654', 'Lavender Avenue', '2637', 'District of Columbia','1480819', '613288', '516180', '14', '29', '42');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Chicago', '54321', 'Marigold Way', '360', 'Texas','1867761', '2735443', '2426913', '11', '24', '43');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Tucson', '10987', 'Narcissus Lane', '962', 'New Jersey','2496377', '2032414', '521183', '3', '11', '44');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Las Vegas', '76543', 'Orchid Street', '2', 'Oregon','623517', '1534416', '987256', '14', '34', '45');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Birmingham', '32109', 'Peony Avenue', '6818', 'District of Columbia','2640661', '3001395', '795774', '5', '3', '46');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Atlanta', '65432', 'Quince Court', '96387', 'West Virginia','3069162', '3983475', '3239968', '7', '10', '47');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Phoenix', '89012', 'Rose Place', '1', 'Texas','1053060', '222136', '650469', '8', '26', '48');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Raleigh', '43210', 'Sunflower Lane', '9', 'California','1182602', '1084618', '1824153', '7', '1', '49');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Austin', '32223', 'Tulip Drive', '32', 'Mississippi','3569901', '3965097', '3961753', '13', '6', '50');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Tucson', '54321', 'Violet Boulevard', '23', 'West Virginia','1223311', '3416879', '2828699', '13', '1', '51');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Dallas', '98765', 'Zinnia Street', '63191', 'Louisiana','3334426', '818787', '2730910', '2', '11', '52');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Jacksonville', '67890', 'Acorn Avenue', '5', 'Illinois','1034490', '808602', '3099678', '10', '23', '53');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Dallas', '45678', 'Bay Road', '3555', 'New York','2676833', '1529399', '3576631', '9', '3', '54');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'San Francisco', '23456', 'Cactus Lane', '2002', 'Florida','1926189', '1878943', '3794081', '2', '7', '55');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Los Angeles', '87654', 'Daisy Boulevard', '5', 'Ohio','3412310', '991939', '2454272', '3', '17', '56');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Dallas', '34567', 'Evergreen Way', '959', 'Colorado','3332773', '1257489', '3179239', '9', '11', '57');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Raleigh', '78901', 'Flamingo Circle', '2630', 'California','2343491', '1806753', '1981665', '5', '5', '58');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Madison', '56789', 'Grove Place', '69514', 'Michigan','135948', '3239556', '2752444', '11', '22', '59');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Raleigh', '21098', 'Holly Street', '83', 'Georgia','1066532', '2803633', '3276789', '15', '5', '60');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Philadelphia', '87654', 'Ivy Avenue', '3', 'Florida','3428501', '1365839', '3889133', '2', '2', '61');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Fargo', '54321', 'Jade Road', '83554', 'New York','765624', '3623332', '2696276', '3', '10', '62');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Miami', '10987', 'Koi Lane', '2470', 'Pennsylvania','3368837', '2806824', '1790692', '13', '34', '63');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Chicago', '76543', 'Lagoon Drive', '922', 'Ohio','380947', '1119212', '1961976', '5', '12', '64');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Raleigh', '32109', 'Meadow Boulevard', '01', 'West Virginia','633599', '3574072', '3422094', '8', '33', '65');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Las Vegas', '65432', 'Nectar Way', '56455', 'Hawaii','2581428', '334981', '1687900', '9', '2', '66');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Chicago', '89012', 'Olive Court', '036', 'Arizona','2139756', '3305039', '1897406', '7', '17', '67');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Houston', '43210', 'Pond Place', '32501', 'Texas','3281722', '1609975', '3777029', '14', '27', '68');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Portland', '67890', 'Quail Lane', '59266', 'New York','1829599', '784775', '351994', '4', '13', '69');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Jacksonville', '21098', 'Ridge Street', '792', 'California','179164', '3662621', '1479567', '2', '25', '70');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Phoenix', '87654', 'Sage Avenue', '5479', 'Maryland','2146987', '3023590', '3770454', '3', '20', '71');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Detroit', '54321', 'Tide Road', '5573', 'Virginia','2355644', '495530', '3933541', '12', '21', '72');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Memphis', '10987', 'Umbrella Lane', '4', 'California','1462196', '1528398', '142668', '15', '32', '73');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Austin', '76543', 'Valley Drive', '7686', 'Arizona','2575590', '3265415', '144444', '1', '26', '74');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'San Francisco', '32109', 'Waterfall Way', '203', 'Texas','975490', '2610651', '2691402', '6', '16', '75');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('1', 'Salem', '65432', 'Xenon Court', '36293', 'Indiana','3248027', '3793099', '1700973', '10', '29', '76');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Denver', '89012', 'Yacht Place', '014', 'Washington','1225994', '112666', '2717683', '11', '35', '77');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'New York', '43210', 'Zenith Lane', '59042', 'Florida','1497465', '1798136', '935104', '7', '9', '78');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Birmingham', '67890', 'Maple Street', '2', 'Pennsylvania','1439451', '299851', '2534691', '4', '28', '79');
INSERT INTO `Listings` (BeingRented, City, ZipCode, Street, HouseNum, State,PrevPriceData, CurrPriceData, PredictedFuturePriceData, AreaId, RealtorID, id) VALUES ('0', 'Jacksonville', '21098', 'Oak Avenue', '782', 'Arizona','1057034', '3112582', '3703315', '8', '7', '80');

INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2042604', '4', '1');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3010276', '7', '2');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3229661', '27', '3');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1964657', '17', '4');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2750342', '11', '5');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2889401', '4', '6');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2933359', '30', '7');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3872738', '2', '8');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('105054', '11', '9');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2983063', '30', '10');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2211140', '14', '11');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3529959', '16', '12');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3876373', '11', '13');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2694108', '22', '14');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2393169', '20', '15');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1420274', '23', '16');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2670725', '20', '17');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('554282', '25', '18');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1365027', '6', '19');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1508928', '13', '20');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1818239', '9', '21');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2540735', '15', '22');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2199887', '28', '23');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('788110', '17', '24');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2339392', '16', '25');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('226968', '2', '26');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1776145', '29', '27');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2999162', '4', '28');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3933281', '10', '29');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2141201', '22', '30');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1488070', '22', '31');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('641142', '14', '32');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3840337', '10', '33');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2172376', '27', '34');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1181577', '12', '35');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1797474', '18', '36');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1990159', '28', '37');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3445304', '9', '38');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3311561', '5', '39');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1429914', '7', '40');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3975986', '5', '41');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3290023', '8', '42');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('218010', '6', '43');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2057896', '29', '44');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3616977', '20', '45');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('272426', '10', '46');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1657247', '9', '47');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2127203', '7', '48');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1166582', '2', '49');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2661986', '20', '50');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1731287', '3', '51');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3582816', '3', '52');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3099889', '9', '53');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2004812', '30', '54');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('335219', '30', '55');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('111577', '22', '56');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2577696', '6', '57');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2262321', '7', '58');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3013165', '27', '59');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('892866', '16', '60');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2083450', '17', '61');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3155211', '12', '62');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1399845', '29', '63');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3513579', '12', '64');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3689652', '25', '65');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1369979', '19', '66');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1526166', '12', '67');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1413841', '18', '68');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3093026', '13', '69');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1011239', '18', '70');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3639411', '26', '71');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('313626', '13', '72');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('910181', '30', '73');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3698060', '11', '74');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1448191', '12', '75');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1639756', '4', '76');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1699455', '20', '77');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1690148', '22', '78');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1176663', '3', '79');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2470864', '26', '80');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3959447', '25', '81');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('289962', '6', '82');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3405847', '9', '83');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1355431', '26', '84');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1689671', '30', '85');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1798176', '9', '86');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2852719', '14', '87');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2087933', '20', '88');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3050521', '5', '89');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3416319', '17', '90');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3475970', '23', '91');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2197374', '30', '92');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('3869824', '2', '93');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1580420', '21', '94');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('545746', '16', '95');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2838480', '22', '96');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2159854', '18', '97');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('912222', '1', '98');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('2809676', '14', '99');
INSERT INTO `offer` (Amount, OfereeId, id) VALUES ('1408396', '10', '100');

INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('28', '7');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('15', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('2', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('13', '13');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('21', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('20', '10');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('21', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('15', '15');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('2', '15');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('29', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('15', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('14', '13');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('28', '1');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('2', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('14', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('30', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('29', '5');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('27', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('12', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('4', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('24', '7');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('26', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('6', '8');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('1', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('24', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('17', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('15', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('9', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('6', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('25', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('26', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('18', '1');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('20', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('29', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('14', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('19', '15');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('12', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('22', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('8', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('9', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('27', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('9', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('8', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('22', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('6', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('18', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('1', '8');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('24', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('15', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('1', '13');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('19', '3');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('10', '5');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('3', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('9', '1');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('13', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('23', '10');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('21', '5');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('14', '8');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('26', '5');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('9', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('26', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('27', '1');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('19', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('23', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('12', '10');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('24', '1');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('14', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('11', '13');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('20', '8');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('22', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('30', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('8', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('15', '5');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('13', '7');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('7', '3');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('3', '15');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('5', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('28', '5');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('10', '4');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('28', '11');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('6', '9');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('1', '7');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('16', '1');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('23', '12');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('17', '3');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('27', '14');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('29', '6');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('27', '10');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('18', '2');
INSERT INTO `Viewed Area` (UserId, AreaId) VALUES ('29', '8');

INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('2', '21');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('8', '33');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('30', '76');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('5', '60');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('27', '1');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('23', '66');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('28', '64');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('10', '34');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('16', '25');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('22', '47');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('8', '29');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('1', '63');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('30', '50');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('6', '74');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('22', '71');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('18', '52');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('9', '65');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('24', '18');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('24', '40');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '59');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('7', '9');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('4', '31');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('15', '7');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('26', '1');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '57');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('12', '53');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('15', '68');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('3', '77');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('24', '69');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '67');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('20', '8');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('17', '11');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('28', '80');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('6', '54');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('5', '7');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('12', '16');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '48');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('5', '73');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('20', '26');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('17', '40');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('2', '12');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('13', '36');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('28', '33');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '9');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('2', '34');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('26', '77');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('13', '1');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('9', '36');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('30', '53');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('20', '13');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('25', '29');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('1', '77');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('12', '24');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('13', '2');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('6', '73');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('13', '13');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('2', '77');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('26', '74');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('12', '46');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('28', '27');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('10', '16');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('17', '54');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('18', '1');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('6', '15');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('22', '69');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('7', '2');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('18', '2');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('25', '48');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '78');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('26', '18');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('16', '6');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('9', '32');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('29', '79');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('13', '60');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('16', '80');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('28', '74');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('3', '60');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('25', '18');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('29', '72');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('26', '6');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('1', '68');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('21', '33');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('5', '17');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('16', '56');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('2', '75');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('22', '28');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('27', '49');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('3', '40');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('4', '50');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('16', '54');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('7', '74');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('17', '77');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('4', '29');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('13', '64');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('7', '26');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('15', '57');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('10', '56');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('5', '66');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('24', '43');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('1', '11');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('17', '79');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('14', '62');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('6', '68');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('2', '1');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('11', '45');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('16', '8');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('8', '34');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('9', '35');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('30', '58');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('26', '42');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('28', '44');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('4', '5');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('23', '9');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('22', '78');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('27', '29');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('25', '36');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('3', '37');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('12', '34');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('18', '54');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('21', '4');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('29', '20');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('19', '3');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('20', '76');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('6', '13');
INSERT INTO `Viewed Listing` (UserId, ListingId) VALUES ('10', '23');

INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('1', '5');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('2', '12');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('3', '26');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('4', '44');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('5', '59');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('6', '33');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('7', '35');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('8', '77');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('9', '45');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('10', '60');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('11', '42');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('12', '8');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('13', '1');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('14', '8');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('15', '72');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('16', '68');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('17', '47');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('18', '26');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('19', '51');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('20', '36');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('21', '18');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('22', '34');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('23', '77');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('24', '31');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('25', '41');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('26', '36');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('27', '38');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('28', '27');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('29', '48');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('30', '43');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('31', '25');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('32', '17');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('33', '76');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('34', '15');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('35', '52');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('36', '4');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('37', '77');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('38', '22');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('39', '62');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('40', '78');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('41', '45');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('42', '23');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('43', '13');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('44', '65');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('45', '51');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('46', '12');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('47', '46');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('48', '33');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('49', '63');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('50', '60');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('51', '53');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('52', '37');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('53', '60');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('54', '71');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('55', '66');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('56', '20');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('57', '65');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('58', '52');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('59', '19');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('60', '3');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('61', '19');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('62', '78');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('63', '9');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('64', '51');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('65', '22');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('66', '11');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('67', '25');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('68', '8');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('69', '68');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('70', '19');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('71', '18');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('72', '30');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('73', '43');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('74', '15');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('75', '52');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('76', '39');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('77', '23');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('78', '74');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('79', '74');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('80', '29');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('81', '27');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('82', '27');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('83', '40');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('84', '15');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('85', '62');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('86', '21');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('87', '77');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('88', '3');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('89', '41');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('90', '43');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('91', '37');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('92', '50');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('93', '65');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('94', '12');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('95', '1');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('96', '51');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('97', '61');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('98', '65');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('99', '75');
INSERT INTO `Listing Offer` (OfferId, ListingId) VALUES ('100', '40');




