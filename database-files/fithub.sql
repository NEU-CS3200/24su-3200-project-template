DROP DATABASE IF EXISTS fithub;
CREATE DATABASE fithub;
USE fithub;

DROP TABLE IF EXISTS Users;
-- USERS TABLE
CREATE TABLE Users (
UserID INT AUTO_INCREMENT PRIMARY KEY,
Name VARCHAR(100) NOT NULL,
Email VARCHAR(255) NOT NULL UNIQUE,
Phone VARCHAR(20) NOT NULL,
Address VARCHAR(255) NOT NULL,
DOB DATE NOT NULL,
Gender VARCHAR(20) NOT NULL,
IsActive BOOLEAN NOT NULL,
Role VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS Announcements;
-- ANNOUNCEMENTS
CREATE TABLE Announcements (
AnnouncementID INT AUTO_INCREMENT PRIMARY KEY,
AnnouncerID INT NOT NULL,
Message TEXT NOT NULL,
AnnouncedAt DATETIME NOT NULL,
FOREIGN KEY (AnnouncerID) REFERENCES Users(UserID)
);

DROP TABLE IF EXISTS AnnouncementsReceived;
-- ANNOUNCEMENTSRECEIVED
CREATE TABLE AnnouncementsReceived (
AnnouncementID INT NOT NULL,
UserID INT NOT NULL,
PRIMARY KEY (AnnouncementID, UserID),
FOREIGN KEY (AnnouncementID) REFERENCES Announcements(AnnouncementID),
FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

DROP TABLE IF EXISTS Items;
-- ITEMS
CREATE TABLE Items (
ItemID INT AUTO_INCREMENT PRIMARY KEY,
Title VARCHAR(255) NOT NULL,
Category VARCHAR(100) NOT NULL,
Description TEXT NOT NULL,
Size VARCHAR(10) NOT NULL,
`Condition` VARCHAR(100) NOT NULL,
IsAvailable BOOLEAN NOT NULL,
OwnerID INT NOT NULL,
ListedAt DATETIME NOT NULL,
`Type` VARCHAR(10) NOT NULL,
FOREIGN KEY (OwnerID) REFERENCES Users(UserID)
);

DROP TABLE IF EXISTS Reports;
-- REPORTS
CREATE TABLE Reports (
ReportID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
Note TEXT NOT NULL,
Severity INT NOT NULL,
Resolved BOOLEAN NOT NULL,
ReporterID INT NOT NULL,
ReportedUser INT NULL,
ReportedItem INT NULL,
ResolverID INT NULL,
ResolvedAt DATETIME NULL,
FOREIGN KEY (ReporterID) REFERENCES Users(UserID),
FOREIGN KEY (ReportedUser) REFERENCES Users(UserID),
FOREIGN KEY (ReportedItem) REFERENCES Items(ItemID),
FOREIGN KEY (ResolverID) REFERENCES Users(UserID)
);

DROP TABLE IF EXISTS Images;
-- IMAGES
CREATE TABLE Images (
ImageID INT AUTO_INCREMENT PRIMARY KEY,
ItemID INT NOT NULL,
ImageURL TEXT NOT NULL,
ImageOrderNum INT NOT NULL,
FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

DROP TABLE IF EXISTS Tags;
-- TAGS
CREATE TABLE Tags (
TagID INT AUTO_INCREMENT PRIMARY KEY,
Title VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS ItemTags;
-- ITEMTAGS
CREATE TABLE ItemTags (
ItemID INT NOT NULL,
TagID INT NOT NULL,
PRIMARY KEY (ItemID, TagID),
FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
FOREIGN KEY (TagID) REFERENCES Tags(TagID)
);

DROP TABLE IF EXISTS Shippings;
-- SHIPPING
CREATE TABLE Shippings (
ShippingID INT AUTO_INCREMENT PRIMARY KEY,
Carrier VARCHAR(100) NOT NULL,
TrackingNum VARCHAR(255) NOT NULL,
DateShipped DATE NOT NULL,
DateArrived DATE NULL
);

DROP TABLE IF EXISTS Orders;
-- ORDERS
CREATE TABLE Orders (
OrderID INT AUTO_INCREMENT PRIMARY KEY,
GivenByID INT NOT NULL,
ReceiverID INT NOT NULL,
CreatedAt DATETIME NOT NULL,
ShippingID INT NULL,
FOREIGN KEY (GivenByID) REFERENCES Users(UserID),
FOREIGN KEY (ReceiverID) REFERENCES Users(UserID),
FOREIGN KEY (ShippingID) REFERENCES Shippings(ShippingID)
);

DROP TABLE IF EXISTS OrderItems;
-- ORDERITEMS
CREATE TABLE OrderItems (
OrderID INT NOT NULL,
ItemID INT NOT NULL,
PRIMARY KEY (OrderID, ItemID),
FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

DROP TABLE IF EXISTS Feedback;
-- FEEDBACK
CREATE TABLE Feedback (
FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
OrderID INT NOT NULL,
Rating INT NOT NULL,
Comment TEXT NOT NULL,
CreatedAt DATETIME NOT NULL,
CreatedByID INT NOT NULL,
FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
FOREIGN KEY (CreatedByID) REFERENCES Users(UserID),
CHECK (Rating BETWEEN 1 AND 5)
);

-- RESET ALL DATA
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE AnnouncementsReceived;
TRUNCATE TABLE ItemTags;
TRUNCATE TABLE OrderItems;
TRUNCATE TABLE Feedback;
TRUNCATE TABLE Reports;
TRUNCATE TABLE Images;
TRUNCATE TABLE Orders;
TRUNCATE TABLE Shippings;
TRUNCATE TABLE Items;
TRUNCATE TABLE Announcements;
TRUNCATE TABLE Tags;
TRUNCATE TABLE Users;

SET FOREIGN_KEY_CHECKS = 1;

-- INSERT USERS
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Aisha Seth', 'aseth@fithub.org', '783-714-6861', '696 Rowland Alley', '1994-03-16', 'Female', true, 'admin');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Blair Williams', 'bwilliams@fithub.org', '607-164-4550', '3 Namekagon Terrace', '1997-11-04', 'Female', true, 'analyst');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Waylen Phipard-Shears', 'wpshears2@fithub.org', '585-571-4741', '46 Doe Crossing Trail', '2000-02-05', 'Male', true, 'admin');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Meggie Aleksankin', 'maleksankin3@stumbleupon.com', '170-363-5841', '9711 Carberry Trail', '2006-09-30', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Kingsly Swires', 'kswires4@desdev.cn', '869-764-4936', '5 Dovetail Court', '2000-01-05', 'Male', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Gilberto Jordison', 'gjordison5@google.com.br', '215-415-1029', '08 Annamark Junction', '2007-11-03', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Atlante Kindall', 'akindall6@about.me', '709-939-0916', '762 Anderson Park', '2000-12-04', 'Bigender', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Alexi Moreinu', 'amoreinu7@dell.com', '979-373-6083', '02727 Luster Park', '2003-02-06', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Milly Gue', 'mgue8@businessweek.com', '879-895-9007', '52 Alpine Terrace', '2006-02-10', 'Polygender', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Doralynn Hamlyn', 'dhamlyn9@fotki.com', '323-337-9508', '813 Debs Trail', '2002-01-25', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Mahmoud Klazenga', 'mklazengaa@jiathis.com', '641-148-8235', '705 Prairie Rose Court', '2001-12-23', 'Male', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Agustin Stickells', 'astickellsb@cnbc.com', '740-855-4464', '13 Myrtle Terrace', '2006-05-19', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Efren Everingham', 'eeveringhamc@reverbnation.com', '191-543-6910', '95491 Goodland Circle', '2001-09-05', 'Agender', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Penn Robilart', 'probilartd@odnoklassniki.ru', '167-291-8605', '1449 Fulton Place', '2007-12-23', 'Male', false, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Hillier Thompkins', 'hthompkinse@vinaora.com', '504-931-0747', '50 Fallview Trail', '2007-08-09', 'Male', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Maryanna Sedgwick', 'msedgwickf@usnews.com', '216-694-7935', '4 Bashford Road', '2006-04-16', 'Female', false, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Quintilla Reimer', 'qreimerg@plala.or.jp', '253-962-6818', '107 Lyons Court', '2007-07-24', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Lurette Matyushenko', 'lmatyushenkoh@woothemes.com', '615-436-3277', '26 Donald Street', '2002-02-22', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Rhona Smissen', 'rsmisseni@statcounter.com', '714-336-8319', '0 Steensland Trail', '2008-05-02', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Lurleen Loody', 'lloodyj@jimdo.com', '624-862-3836', '9524 Ohio Alley', '2001-09-15', 'Agender', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Parrnell O''Docherty', 'podochertyk@cnet.com', '403-914-1659', '84 Garrison Alley', '2007-02-06', 'Male', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Jarret Brimilcome', 'jbrimilcomel@reverbnation.com', '230-152-1964', '6 Prentice Park', '2000-10-10', 'Male', false, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Imogene Waddam', 'iwaddamm@soundcloud.com', '916-806-9329', '52632 Hauk Alley', '2005-08-04', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Zebadiah Corthes', 'zcorthesn@gnu.org', '202-670-1925', '9 Shelley Court', '2003-08-07', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Jacqui De Wolfe', 'jdeo@sourceforge.net', '915-247-4278', '49958 Brown Way', '2007-03-24', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Rutter Bartolomeo', 'rbartolomeop@amazonaws.com', '529-202-7689', '47026 Merchant Drive', '2006-04-29', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Lana Ferriday', 'lferridayq@dailymail.co.uk', '748-446-1428', '89 Sachs Street', '2008-10-12', 'Non-binary', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Caitlin Cadlock', 'ccadlockr@japanpost.jp', '202-514-4711', '5024 Riverside Way', '2008-08-08', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Doria True', 'dtrues@hatena.ne.jp', '673-877-5502', '935 Old Shore Place', '2004-12-12', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Willamina Guite', 'wguitet@apple.com', '879-495-7973', '5 Magdeline Road', '2007-12-14', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Halli Conneely', 'hconneelyu@weebly.com', '412-281-1093', '7 Swallow Park', '2005-05-04', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Rivkah Truscott', 'rtruscottv@wikispaces.com', '969-724-2894', '6534 Schmedeman Terrace', '2004-09-15', 'Female', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Germana Praill', 'gpraillw@webs.com', '418-980-7134', '8847 Prairieview Hill', '2003-09-10', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Andrej Simants', 'asimantsx@tripod.com', '938-331-1813', '455 Sunfield Hill', '2004-05-03', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Arabele Kinningley', 'akinningleyy@biglobe.ne.jp', '209-478-2254', '1184 Northridge Crossing', '2007-01-22', 'Female', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Bryant Fernao', 'bfernaoz@canalblog.com', '338-119-6662', '0 Melody Alley', '2001-12-14', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Granthem Klossek', 'gklossek10@tumblr.com', '796-347-3135', '5 Warbler Trail', '2004-11-07', 'Male', true, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Delmar Rigbye', 'drigbye11@wisc.edu', '434-650-1264', '15275 Elgar Road', '2007-06-04', 'Male', true, 'taker');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Kimmie Bickersteth', 'kbickersteth12@bizjournals.com', '975-673-6496', '39909 Iowa Junction', '2007-12-02', 'Bigender', false, 'swapper');
insert into Users (Name, Email, Phone, Address, DOB, Gender, IsActive, Role) values ('Inger Valeri', 'ivaleri13@baidu.com', '364-888-1308', '7012 Oak Terrace', '2006-04-25', 'Male', true, 'taker');
SELECT * FROM Users;

-- INSERT ANNOUNCEMENTS
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Join our upcoming virtual swap meet on Saturday!', '2025-09-28 13:21:51');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-08-01 16:36:36');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Pro tip: Use aesthetic tags like Y2K or Coquette or Streetwear.', '2025-03-11 20:58:34');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Stay tuned for exclusive discounts from our partner brands.', '2025-11-06 23:10:44');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Pro tip: Use aesthetic tags like Y2K or Coquette or Streetwear.', '2025-09-17 04:32:57');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Join our upcoming virtual swap meet on Saturday!', '2025-11-04 15:55:27');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Stay tuned for exclusive discounts from our partner brands.', '2025-10-25 15:57:13');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Check out our instagram for styling tips and trend forecasts.', '2025-07-17 18:26:16');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Pro tip: Use aesthetic tags like Y2K or Coquette or Streetwear.', '2025-05-22 00:51:36');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Welcome to FitHub! List your pre-loved fits and swap with the community.', '2025-11-04 22:59:25');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Check out our instagram for styling tips and trend forecasts.', '2025-01-11 08:47:13');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Join our upcoming virtual swap meet on Saturday!', '2025-08-22 18:09:21');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Pro tip: Use aesthetic tags like Y2K or Coquette or Streetwear.', '2025-10-26 06:51:08');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-07-19 03:52:09');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Welcome to FitHub! List your pre-loved fits and swap with the community.', '2025-04-05 13:12:29');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-06-17 01:28:50');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-05-28 07:40:04');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Welcome to FitHub! List your pre-loved fits and swap with the community.', '2025-08-08 08:40:40');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Check out our instagram for styling tips and trend forecasts.', '2025-09-28 00:20:16');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Congratulations on completing your first swap! Keep it up!', '2025-05-21 16:43:09');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Welcome to FitHub! List your pre-loved fits and swap with the community.', '2024-12-19 23:24:03');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-06-19 04:43:36');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Maintenance scheduled for tomorrow at 2 PM.', '2025-08-27 12:21:49');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Don''t forget to update your profile with your latest fits!', '2025-01-15 02:08:41');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Pro tip: Use aesthetic tags like Y2K or Coquette or Streetwear.', '2025-03-21 12:25:44');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Join our upcoming virtual swap meet on Saturday!', '2025-08-26 14:55:50');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Maintenance scheduled for tomorrow at 2 PM.', '2025-11-13 01:45:41');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-01-31 00:23:15');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2024-12-13 22:59:34');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Maintenance scheduled for tomorrow at 2 PM.', '2024-12-22 07:56:02');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Stay tuned for exclusive discounts from our partner brands.', '2025-08-30 14:14:36');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Check out our instagram for styling tips and trend forecasts.', '2025-02-03 15:17:06');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Welcome to FitHub! List your pre-loved fits and swap with the community.', '2025-08-11 00:50:35');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Don''t forget to update your profile with your latest fits!', '2025-02-27 07:22:15');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Congratulations on completing your first swap! Keep it up!', '2025-11-02 16:02:45');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Congratulations on completing your first swap! Keep it up!', '2025-11-03 00:38:50');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Join our upcoming virtual swap meet on Saturday!', '2025-06-16 17:46:37');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Pro tip: Use aesthetic tags like Y2K or Coquette or Streetwear.', '2025-06-29 15:13:14');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (1, 'Stay tuned for exclusive discounts from our partner brands.', '2025-07-25 01:21:11');
insert into Announcements (AnnouncerID, Message, AnnouncedAt) values (3, 'Congratulations on completing your first swap! Keep it up!', '2025-06-17 07:06:11');
SELECT * FROM Announcements;

-- INSERT ANNOUNCEMENTS RECEIVED
insert into AnnouncementsReceived (AnnouncementID, UserID) values (36, 39);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (17, 3);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (19, 20);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (14, 4);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (8, 4);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (10, 13);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (40, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (2, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (7, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (25, 16);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (7, 6);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (34, 34);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (30, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (26, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (29, 11);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (22, 23);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (1, 40);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (6, 30);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (20, 21);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (14, 30);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (7, 33);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (38, 19);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (32, 17);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (23, 10);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (17, 18);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (3, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 24);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (1, 10);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (22, 9);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (39, 37);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (16, 32);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (16, 14);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (33, 27);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (5, 25);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (29, 5);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (31, 21);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (16, 36);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (32, 36);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (5, 36);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (30, 31);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (10, 38);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (31, 40);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (31, 3);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (12, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (16, 18);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (16, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (4, 34);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (24, 37);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 9);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (13, 36);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (38, 10);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (30, 30);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (2, 18);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (5, 19);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (32, 35);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (11, 9);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (4, 13);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (37, 11);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (7, 17);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (34, 5);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (24, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 6);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (13, 38);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (7, 37);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (33, 6);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (24, 6);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 28);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (25, 30);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (20, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (25, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (25, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (13, 39);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (23, 12);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (40, 4);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (13, 11);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (13, 9);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (34, 19);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (34, 12);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (14, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (19, 10);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 14);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (19, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (40, 38);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (39, 33);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (30, 35);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (4, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (26, 6);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (5, 9);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (26, 31);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (1, 8);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (32, 12);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (36, 8);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 4);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (9, 11);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (16, 20);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (8, 19);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 11);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (1, 18);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (27, 9);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (32, 19);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (11, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (33, 35);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (12, 38);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (14, 14);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (19, 31);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (14, 23);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (6, 29);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (6, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (33, 14);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (17, 5);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (23, 39);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (26, 5);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (9, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (22, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (19, 38);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (8, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (1, 16);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (12, 33);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (3, 12);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (23, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (3, 30);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (30, 24);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (28, 33);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (2, 4);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (15, 23);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 37);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (13, 37);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (22, 17);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (7, 16);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (1, 35);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (23, 4);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (12, 23);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 26);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 25);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (17, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (28, 11);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (40, 7);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (24, 24);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (17, 24);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (25, 31);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 5);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 16);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (31, 37);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (30, 8);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (25, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 22);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (6, 35);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (9, 31);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (22, 16);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (10, 39);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (35, 10);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (40, 15);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (18, 25);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (10, 34);
insert into AnnouncementsReceived (AnnouncementID, UserID) values (21, 34);
SELECT * FROM AnnouncementsReceived;

-- INSERT ITEMS
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Converse Chuck Taylor', 'shoes', 'Red high tops, some wear on soles', 'M', 'Good', true, 8, '2025-02-13 16:45:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Vintage Band Tee', 't-shirt', 'Nirvana concert tee from the 90s', 'M', 'Good', true, 6, '2025-02-14 10:30:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Leather Moto Jacket', 'jacket', 'Black leather jacket, slightly worn', 'L', 'Very good', true, 4, '2025-02-14 13:00:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Floral Midi Dress', 'dress', 'Spring floral pattern, never worn', 'M', 'Excellent', true, 5, '2025-02-15 11:20:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('High-Waisted Mom Jeans', 'jeans', 'Light wash, straight leg fit', 'M', 'Good', true, 6, '2025-02-15 15:05:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Oversized Knit Sweater', 'sweater', 'Cream chunky knit, cozy for winter', 'L', 'Very good', true, 7, '2025-02-16 09:45:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Black Chelsea Boots', 'shoes', 'Leather ankle boots, small scuff on heel', 'M', 'Good', true, 8, '2025-02-16 14:10:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Puffer Winter Coat', 'coat', 'Long black puffer, very warm with hood', 'L', 'Excellent', true, 9, '2025-02-17 10:00:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Corduroy Mini Skirt', 'skirt', 'Brown corduroy mini skirt with pockets', 'S', 'Very good', true, 10, '2025-02-17 16:20:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Graphic Hoodie', 'hoodie', 'Gray hoodie with retro print on back', 'M', 'Good', true, 11, '2025-02-18 13:40:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Running Sneakers', 'shoes', 'White running shoes, lightly used', 'M', 'Good', false, 12, '2025-02-18 18:05:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Plaid Flannel Shirt', 'shirt', 'Red and navy flannel, soft fabric', 'M', 'Very good', true, 13, '2025-02-19 09:25:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Denim Jacket', 'jacket', 'Classic blue denim jacket, slightly cropped', 'M', 'Excellent', false, 14, '2025-02-19 14:50:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Wool Winter Coat', 'coat', 'Navy blue wool winter coat, excellent condition', 'L', 'Excellent', false, 12, '2025-10-25 10:00:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Silk Blouse', 'blouse', 'Ivory silk button-up, barely worn', 'M', 'Excellent', true, 15, '2025-02-20 11:15:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Wide-Leg Trousers', 'pants', 'Black high-waisted wide-leg dress pants', 'M', 'Very good', false, 16, '2025-02-20 17:30:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Striped Long-Sleeve Tee', 't-shirt', 'Navy and white striped tee with boat neck', 'S', 'Good', true, 17, '2025-02-21 10:10:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Raincoat', 'coat', 'Yellow waterproof raincoat with hood', 'M', 'Very good', true, 18, '2025-02-21 13:55:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Black Leggings', 'pants', 'High-rise leggings that are squat-proof', 'M', 'Good', true, 19, '2025-02-22 09:05:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Chunky Platform Sandals', 'shoes', 'Black platform sandals, worn twice', 'M', 'Excellent', true, 20, '2025-02-22 15:45:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Cable Knit Cardigan', 'sweater', 'Olive green button-up cable knit cardigan', 'M', 'Very good', true, 21, '2025-02-23 12:20:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Bodycon Party Dress', 'dress', 'Black bodycon dress with square neckline', 'S', 'Good', true, 22, '2025-02-23 18:40:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Tennis Skirt', 'skirt', 'White pleated tennis skirt, small stain near hem', 'S', 'Fair', true, 23, '2025-02-24 09:35:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Oversized Blazer', 'blazer', 'Gray checkered blazer with boyfriend fit', 'M', 'Very good', true, 24, '2025-02-24 14:25:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Fleece Quarter-Zip', 'sweater', 'Navy fleece quarter-zip, super soft', 'L', 'Good', true, 25, '2025-02-25 08:50:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Cargo Pants', 'pants', 'Khaki cargo pants with side pockets', 'M', 'Good', true, 26, '2025-02-25 16:05:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Combat Boots', 'shoes', 'Black lace-up combat boots, broken in but solid', 'M', 'Fair', true, 27, '2025-02-26 11:40:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Maxi Skirt', 'skirt', 'Flowy floral maxi skirt with side slit', 'M', 'Very good', false, 28, '2025-02-26 17:15:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Cropped Tank Top', 'tank top', 'Black ribbed cropped tank top', 'S', 'Excellent', true, 29, '2025-02-27 10:05:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Linen Button-Up Shirt', 'shirt', 'Beige linen button-up, relaxed fit', 'L', 'Very good', true, 30, '2025-02-27 15:20:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Track Jacket', 'jacket', 'Vintage blue track jacket with white stripes', 'M', 'Good', true, 31, '2025-02-28 09:55:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('High-Neck Sweater Dress', 'dress', 'Camel knit sweater dress, midi length', 'M', 'Excellent', true, 32, '2025-02-28 18:10:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Slip Dress', 'dress', 'Sage green satin slip dress', 'S', 'Very good', true, 33, '2025-03-01 11:30:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Baggy Sweatpants', 'pants', 'Gray sweatpants with drawstring waist', 'M', 'Good', true, 34, '2025-03-01 16:45:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Sherpa Lined Denim Jacket', 'jacket', 'Blue denim jacket with cream sherpa lining', 'L', 'Very good', true, 35, '2025-03-02 10:15:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Athletic Shorts', 'shorts', 'Black running shorts with built-in liner', 'M', 'Good', true, 36, '2025-03-02 14:35:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Turtleneck Top', 'top', 'Black fitted turtleneck, great for layering', 'S', 'Excellent', true, 37, '2025-03-03 09:25:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Oversized Graphic Tee', 't-shirt', 'Washed black tee with festival graphic', 'L', 'Good', true, 38, '2025-03-03 13:50:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Suede Ankle Boots', 'shoes', 'Tan suede ankle boots, minor crease on toe', 'M', 'Very good', true, 39, '2025-03-04 11:05:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Polo Shirt', 'shirt', 'Forest green polo shirt, slightly faded collar', 'M', 'Fair', true, 40, '2025-03-04 17:40:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Quilted Vest', 'vest', 'Black quilted vest, lightweight layering piece', 'M', 'Good', true, 4, '2025-03-05 10:55:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Vintage Denim Jacket', 'jacket', 'Classic blue denim jacket with patches', 'M', 'Very good', true, 6, '2025-12-07 11:15:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('White Sneakers', 'shoes', 'Clean white canvas sneakers, barely worn', 'M', 'Excellent', true, 10, '2025-12-07 08:15:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Black Midi Dress', 'dress', 'Elegant black midi dress, perfect for events', 'S', 'Excellent', true, 14, '2025-12-07 05:15:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Cozy Cardigan', 'sweater', 'Soft beige cardigan, great for layering', 'L', 'Very good', true, 16, '2025-12-07 01:15:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Leather Belt', 'accessories', 'Brown leather belt with silver buckle', 'M', 'Good', true, 18, '2025-12-06 19:15:00', 'take');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Wool Winter Coat', 'coat', 'Navy blue wool winter coat, excellent condition', 'L', 'Excellent', false, 12, '2025-10-25 10:00:00', 'take');
SELECT * FROM Items;

-- INSERT REPORTS
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 5, true, 18, null, 26, 3, '2025-03-31 21:13:09');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 2, true, 9, null, 17, 1, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 5, true, 14, null, 4, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 4, true, 8, null, 4, null, '2025-02-02 04:29:51');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 5, true, 26, null, 5, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 5, true, 11, null, 37, 3, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 4, false, 4, null, 26, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 1, true, 34, null, 30, 3, '2024-12-27 00:27:56');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 1, true, 7, null, 27, 3, '2025-01-18 18:59:23');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 3, true, 14, null, 16, 3, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 4, false, 34, 21, 3, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 3, true, 1, null, 25, 3, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 3, true, 35, 33, 30, null, '2025-08-25 17:10:51');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 5, true, 6, null, 39, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 3, false, 22, null, 13, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 4, false, 7, null, 5, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 4, true, 14, null, 2, 1, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 3, false, 27, null, 28, 3, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 5, true, 27, null, 7, null, '2025-03-23 04:42:22');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 5, false, 3, null, 27, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 3, true, 16, null, 20, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 2, false, 33, null, 40, 3, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 4, true, 31, null, 22, null, '2025-06-04 18:25:33');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 4, false, 38, 23, 33, 3, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 1, false, 31, null, 34, 1, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 1, true, 6, null, 11, null, '2024-12-21 05:50:41');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 1, true, 9, null, 10, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 4, false, 26, null, 8, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 1, true, 4, null, 8, 3, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 1, false, 25, null, 4, 3, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 4, false, 5, null, 25, 1, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Duplicate listing issue', 4, true, 40, 11, 33, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 2, false, 21, null, 38, null, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Small stain near hem', 4, true, 11, null, 20, null, '2025-09-06 09:53:11');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 5, true, 18, null, 18, null, '2025-01-01 00:00:00');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 2, false, 36, null, 17, 3, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 5, false, 17, 32, 7, 1, null);
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Hoodie had a loose thread', 4, true, 25, 29, 21, 1, '2025-02-22 01:12:01');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Admin flagged due to inappropriate content', 3, true, 35, null, 38, 1, '2025-10-14 07:18:46');
insert into Reports (Note, Severity, Resolved, ReporterID, ReportedUser, ReportedItem, ResolverID, ResolvedAt) values ('Jeans arrived more faded', 5, true, 3, null, 37, null, '2025-10-10 17:59:23');
SELECT * FROM Reports;

-- INSERT IMAGES
insert into Images (ItemID, ImageURL, ImageOrderNum) values (1, 'https://example.com/image1.jpg', 16);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (2, 'https://example.com/image2.jpg', 29);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (3, 'https://example.com/image3.jpg', 29);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (4, 'https://example.com/image4.jpg', 37);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (5, 'https://example.com/image5.jpg', 28);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (6, 'https://example.com/image6.jpg', 10);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (7, 'https://example.com/image7.jpg', 39);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (8, 'https://example.com/image8.jpg', 4);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (9, 'https://example.com/image9.jpg', 20);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (10, 'https://example.com/image10.jpg', 25);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (11, 'https://example.com/image11.jpg', 3);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (12, 'https://example.com/image12.jpg', 30);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (13, 'https://example.com/image13.jpg', 18);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (14, 'https://example.com/image14.jpg', 17);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (15, 'https://example.com/image15.jpg', 23);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (16, 'https://example.com/image16.jpg', 12);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (17, 'https://example.com/image17.jpg', 37);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (18, 'https://example.com/image18.jpg', 32);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (19, 'https://example.com/image19.jpg', 8);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (20, 'https://example.com/image20.jpg', 27);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (21, 'https://example.com/image21.jpg', 6);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (22, 'https://example.com/image22.jpg', 11);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (23, 'https://example.com/image23.jpg', 36);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (24, 'https://example.com/image24.jpg', 40);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (25, 'https://example.com/image25.jpg', 28);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (26, 'https://example.com/image26.jpg', 30);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (27, 'https://example.com/image27.jpg', 4);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (28, 'https://example.com/image28.jpg', 34);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (29, 'https://example.com/image29.jpg', 19);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (30, 'https://example.com/image30.jpg', 26);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (31, 'https://example.com/image31.jpg', 19);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (32, 'https://example.com/image32.jpg', 26);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (33, 'https://example.com/image33.jpg', 39);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (34, 'https://example.com/image34.jpg', 26);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (35, 'https://example.com/image35.jpg', 40);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (36, 'https://example.com/image36.jpg', 4);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (37, 'https://example.com/image37.jpg', 24);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (38, 'https://example.com/image38.jpg', 14);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (39, 'https://example.com/image39.jpg', 20);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (40, 'https://example.com/image40.jpg', 33);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (1, 'https://example.com/image41.jpg', 7);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (2, 'https://example.com/image42.jpg', 22);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (3, 'https://example.com/image43.jpg', 15);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (4, 'https://example.com/image44.jpg', 33);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (5, 'https://example.com/image45.jpg', 18);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (6, 'https://example.com/image46.jpg', 9);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (7, 'https://example.com/image47.jpg', 31);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (8, 'https://example.com/image48.jpg', 13);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (9, 'https://example.com/image49.jpg', 35);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (10, 'https://example.com/image50.jpg', 3);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (11, 'https://example.com/image51.jpg', 21);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (12, 'https://example.com/image52.jpg', 30);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (13, 'https://example.com/image53.jpg', 16);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (14, 'https://example.com/image54.jpg', 11);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (15, 'https://example.com/image55.jpg', 27);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (16, 'https://example.com/image56.jpg', 8);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (17, 'https://example.com/image57.jpg', 40);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (18, 'https://example.com/image58.jpg', 17);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (19, 'https://example.com/image59.jpg', 24);
insert into Images (ItemID, ImageURL, ImageOrderNum) values (20, 'https://example.com/image60.jpg', 6);
SELECT * FROM Images;

-- INSERT TAGS
insert into Tags (Title) values ('Y2K');
insert into Tags (Title) values ('Chic');
insert into Tags (Title) values ('Bohemian');
insert into Tags (Title) values ('Preppy');
insert into Tags (Title) values ('Retro');
insert into Tags (Title) values ('Eclectic');
insert into Tags (Title) values ('Preppy');
insert into Tags (Title) values ('Sporty');
insert into Tags (Title) values ('Eclectic');
insert into Tags (Title) values ('Edgy');
insert into Tags (Title) values ('Minimalist');
insert into Tags (Title) values ('Sophisticated');
insert into Tags (Title) values ('Bohemian');
insert into Tags (Title) values ('Sporty');
insert into Tags (Title) values ('Chic');
insert into Tags (Title) values ('Chic');
insert into Tags (Title) values ('Urban');
insert into Tags (Title) values ('Y2K');
insert into Tags (Title) values ('Preppy');
insert into Tags (Title) values ('Sophisticated');
insert into Tags (Title) values ('Minimalist');
insert into Tags (Title) values ('Sophisticated');
insert into Tags (Title) values ('Sporty');
insert into Tags (Title) values ('Minimalist');
insert into Tags (Title) values ('Urban');
insert into Tags (Title) values ('Edgy');
insert into Tags (Title) values ('Chic');
insert into Tags (Title) values ('Edgy');
insert into Tags (Title) values ('Eclectic');
insert into Tags (Title) values ('Y2K');
insert into Tags (Title) values ('Y2K');
insert into Tags (Title) values ('Minimalist');
insert into Tags (Title) values ('Retro');
insert into Tags (Title) values ('Urban');
insert into Tags (Title) values ('Chic');
insert into Tags (Title) values ('Y2K');
insert into Tags (Title) values ('Sophisticated');
insert into Tags (Title) values ('Preppy');
insert into Tags (Title) values ('Edgy');
insert into Tags (Title) values ('Eclectic');
SELECT * FROM Tags;

-- INSERT ITEMTAGS
insert into ItemTags (ItemID, TagID) values (1, 1);
insert into ItemTags (ItemID, TagID) values (2, 2);
insert into ItemTags (ItemID, TagID) values (2, 9);
insert into ItemTags (ItemID, TagID) values (3, 10);
insert into ItemTags (ItemID, TagID) values (4, 4);
insert into ItemTags (ItemID, TagID) values (4, 11);
insert into ItemTags (ItemID, TagID) values (5, 5);
insert into ItemTags (ItemID, TagID) values (5, 12);
insert into ItemTags (ItemID, TagID) values (5, 19);
insert into ItemTags (ItemID, TagID) values (6, 6);
insert into ItemTags (ItemID, TagID) values (6, 13);
insert into ItemTags (ItemID, TagID) values (6, 20);
insert into ItemTags (ItemID, TagID) values (7, 7);
insert into ItemTags (ItemID, TagID) values (7, 14);
insert into ItemTags (ItemID, TagID) values (7, 21);
insert into ItemTags (ItemID, TagID) values (8, 8);
insert into ItemTags (ItemID, TagID) values (8, 15);
insert into ItemTags (ItemID, TagID) values (8, 22);
insert into ItemTags (ItemID, TagID) values (9, 9);
insert into ItemTags (ItemID, TagID) values (9, 16);
insert into ItemTags (ItemID, TagID) values (9, 23);
insert into ItemTags (ItemID, TagID) values (10, 10);
insert into ItemTags (ItemID, TagID) values (10, 17);
insert into ItemTags (ItemID, TagID) values (10, 24);
insert into ItemTags (ItemID, TagID) values (11, 11);
insert into ItemTags (ItemID, TagID) values (11, 18);
insert into ItemTags (ItemID, TagID) values (11, 25);
insert into ItemTags (ItemID, TagID) values (12, 12);
insert into ItemTags (ItemID, TagID) values (12, 19);
insert into ItemTags (ItemID, TagID) values (12, 26);
insert into ItemTags (ItemID, TagID) values (13, 13);
insert into ItemTags (ItemID, TagID) values (13, 20);
insert into ItemTags (ItemID, TagID) values (13, 27);
insert into ItemTags (ItemID, TagID) values (14, 14);
insert into ItemTags (ItemID, TagID) values (14, 21);
insert into ItemTags (ItemID, TagID) values (14, 28);
insert into ItemTags (ItemID, TagID) values (14, 35);
insert into ItemTags (ItemID, TagID) values (15, 15);
insert into ItemTags (ItemID, TagID) values (15, 22);
insert into ItemTags (ItemID, TagID) values (15, 29);
insert into ItemTags (ItemID, TagID) values (15, 36);
insert into ItemTags (ItemID, TagID) values (16, 16);
insert into ItemTags (ItemID, TagID) values (16, 23);
insert into ItemTags (ItemID, TagID) values (16, 30);
insert into ItemTags (ItemID, TagID) values (16, 37);
insert into ItemTags (ItemID, TagID) values (17, 17);
insert into ItemTags (ItemID, TagID) values (17, 24);
insert into ItemTags (ItemID, TagID) values (17, 31);
insert into ItemTags (ItemID, TagID) values (17, 38);
insert into ItemTags (ItemID, TagID) values (18, 18);
insert into ItemTags (ItemID, TagID) values (18, 25);
insert into ItemTags (ItemID, TagID) values (18, 32);
insert into ItemTags (ItemID, TagID) values (18, 39);
insert into ItemTags (ItemID, TagID) values (19, 19);
insert into ItemTags (ItemID, TagID) values (19, 26);
insert into ItemTags (ItemID, TagID) values (19, 33);
insert into ItemTags (ItemID, TagID) values (19, 40);
insert into ItemTags (ItemID, TagID) values (20, 20);
insert into ItemTags (ItemID, TagID) values (20, 27);
insert into ItemTags (ItemID, TagID) values (20, 34);
insert into ItemTags (ItemID, TagID) values (20, 1);
insert into ItemTags (ItemID, TagID) values (21, 21);
insert into ItemTags (ItemID, TagID) values (21, 28);
insert into ItemTags (ItemID, TagID) values (21, 35);
insert into ItemTags (ItemID, TagID) values (21, 2);
insert into ItemTags (ItemID, TagID) values (22, 22);
insert into ItemTags (ItemID, TagID) values (22, 29);
insert into ItemTags (ItemID, TagID) values (22, 36);
insert into ItemTags (ItemID, TagID) values (22, 3);
insert into ItemTags (ItemID, TagID) values (23, 23);
insert into ItemTags (ItemID, TagID) values (23, 30);
insert into ItemTags (ItemID, TagID) values (23, 37);
insert into ItemTags (ItemID, TagID) values (23, 4);
insert into ItemTags (ItemID, TagID) values (23, 11);
insert into ItemTags (ItemID, TagID) values (24, 24);
insert into ItemTags (ItemID, TagID) values (24, 31);
insert into ItemTags (ItemID, TagID) values (24, 38);
insert into ItemTags (ItemID, TagID) values (24, 5);
insert into ItemTags (ItemID, TagID) values (24, 12);
insert into ItemTags (ItemID, TagID) values (25, 25);
insert into ItemTags (ItemID, TagID) values (25, 32);
insert into ItemTags (ItemID, TagID) values (25, 39);
insert into ItemTags (ItemID, TagID) values (25, 6);
insert into ItemTags (ItemID, TagID) values (25, 13);
insert into ItemTags (ItemID, TagID) values (26, 26);
insert into ItemTags (ItemID, TagID) values (26, 33);
insert into ItemTags (ItemID, TagID) values (26, 40);
insert into ItemTags (ItemID, TagID) values (26, 7);
insert into ItemTags (ItemID, TagID) values (26, 14);
insert into ItemTags (ItemID, TagID) values (27, 27);
insert into ItemTags (ItemID, TagID) values (27, 34);
insert into ItemTags (ItemID, TagID) values (27, 1);
insert into ItemTags (ItemID, TagID) values (27, 8);
insert into ItemTags (ItemID, TagID) values (27, 15);
insert into ItemTags (ItemID, TagID) values (28, 28);
insert into ItemTags (ItemID, TagID) values (28, 35);
insert into ItemTags (ItemID, TagID) values (28, 2);
insert into ItemTags (ItemID, TagID) values (28, 9);
insert into ItemTags (ItemID, TagID) values (28, 16);
insert into ItemTags (ItemID, TagID) values (29, 29);
insert into ItemTags (ItemID, TagID) values (29, 36);
insert into ItemTags (ItemID, TagID) values (29, 3);
insert into ItemTags (ItemID, TagID) values (29, 10);
insert into ItemTags (ItemID, TagID) values (29, 17);
insert into ItemTags (ItemID, TagID) values (30, 30);
insert into ItemTags (ItemID, TagID) values (30, 37);
insert into ItemTags (ItemID, TagID) values (30, 4);
insert into ItemTags (ItemID, TagID) values (30, 11);
insert into ItemTags (ItemID, TagID) values (30, 18);
insert into ItemTags (ItemID, TagID) values (31, 31);
insert into ItemTags (ItemID, TagID) values (31, 38);
insert into ItemTags (ItemID, TagID) values (31, 5);
insert into ItemTags (ItemID, TagID) values (31, 12);
insert into ItemTags (ItemID, TagID) values (31, 19);
insert into ItemTags (ItemID, TagID) values (32, 32);
insert into ItemTags (ItemID, TagID) values (32, 39);
insert into ItemTags (ItemID, TagID) values (32, 6);
insert into ItemTags (ItemID, TagID) values (32, 13);
insert into ItemTags (ItemID, TagID) values (32, 20);
insert into ItemTags (ItemID, TagID) values (33, 33);
insert into ItemTags (ItemID, TagID) values (33, 40);
insert into ItemTags (ItemID, TagID) values (33, 7);
insert into ItemTags (ItemID, TagID) values (33, 14);
insert into ItemTags (ItemID, TagID) values (33, 21);
insert into ItemTags (ItemID, TagID) values (34, 34);
insert into ItemTags (ItemID, TagID) values (34, 1);
insert into ItemTags (ItemID, TagID) values (34, 8);
insert into ItemTags (ItemID, TagID) values (34, 15);
insert into ItemTags (ItemID, TagID) values (34, 22);
insert into ItemTags (ItemID, TagID) values (35, 35);
insert into ItemTags (ItemID, TagID) values (35, 2);
insert into ItemTags (ItemID, TagID) values (35, 9);
insert into ItemTags (ItemID, TagID) values (35, 16);
insert into ItemTags (ItemID, TagID) values (35, 23);
insert into ItemTags (ItemID, TagID) values (36, 36);
insert into ItemTags (ItemID, TagID) values (36, 3);
insert into ItemTags (ItemID, TagID) values (36, 10);
insert into ItemTags (ItemID, TagID) values (36, 17);
insert into ItemTags (ItemID, TagID) values (36, 24);
insert into ItemTags (ItemID, TagID) values (37, 37);
insert into ItemTags (ItemID, TagID) values (37, 4);
insert into ItemTags (ItemID, TagID) values (37, 11);
insert into ItemTags (ItemID, TagID) values (37, 18);
insert into ItemTags (ItemID, TagID) values (37, 25);
insert into ItemTags (ItemID, TagID) values (38, 38);
insert into ItemTags (ItemID, TagID) values (38, 5);
insert into ItemTags (ItemID, TagID) values (38, 12);
insert into ItemTags (ItemID, TagID) values (38, 19);
insert into ItemTags (ItemID, TagID) values (38, 26);
insert into ItemTags (ItemID, TagID) values (39, 39);
insert into ItemTags (ItemID, TagID) values (39, 6);
insert into ItemTags (ItemID, TagID) values (39, 13);
insert into ItemTags (ItemID, TagID) values (39, 20);
insert into ItemTags (ItemID, TagID) values (39, 27);
insert into ItemTags (ItemID, TagID) values (40, 40);
insert into ItemTags (ItemID, TagID) values (40, 7);
insert into ItemTags (ItemID, TagID) values (40, 14);
insert into ItemTags (ItemID, TagID) values (40, 21);
insert into ItemTags (ItemID, TagID) values (40, 28);
insert into ItemTags (ItemID, TagID) values (41, 10);
insert into ItemTags (ItemID, TagID) values (41, 24);
insert into ItemTags (ItemID, TagID) values (42, 11);
insert into ItemTags (ItemID, TagID) values (42, 15);
insert into ItemTags (ItemID, TagID) values (43, 15);
insert into ItemTags (ItemID, TagID) values (43, 28);
insert into ItemTags (ItemID, TagID) values (44, 15);
insert into ItemTags (ItemID, TagID) values (44, 22);
SELECT * FROM ItemTags;

-- INSERT SHIPPINGS
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '111918230', '2025-10-12', '2025-04-07');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '065201611', '2025-03-23', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '071122535', '2025-02-16', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '043308620', '2025-11-27', '2025-02-06');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '084309015', '2025-02-14', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '091902049', '2025-03-24', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '322280485', '2025-05-10', '2024-12-21');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '091803818', '2025-09-21', '2025-10-06');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '054001725', '2025-11-12', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '271070791', '2025-03-03', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '111909825', '2025-02-14', '2025-07-19');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '082903497', '2025-02-11', '2025-01-14');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '053207766', '2025-02-18', '2025-09-19');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '042206503', '2025-07-20', '2025-03-23');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '082903536', '2025-01-02', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '111912197', '2025-04-14', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '072401048', '2025-06-30', '2025-09-14');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '121142850', '2025-01-07', '2025-01-05');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '063104668', '2025-04-03', '2024-12-31');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '071923190', '2025-02-14', '2025-01-02');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '071925350', '2024-12-30', '2025-10-01');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '082908560', '2025-10-25', '2024-12-22');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '081006201', '2025-05-04', '2024-12-04');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '113114595', '2025-11-10', '2024-12-08');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '091400606', '2025-04-06', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '044103523', '2025-11-17', '2025-08-04');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '081206496', '2025-09-20', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '081204281', '2025-06-29', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '061105232', '2025-10-17', '2024-12-07');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '102103630', '2025-01-10', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '072412778', '2025-04-10', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '102101111', '2025-05-11', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '113123625', '2025-06-06', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '101113935', '2025-03-19', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '031317636', '2024-12-20', '2025-08-27');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '125107079', '2025-10-28', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '123103606', '2025-03-15', '2024-12-17');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '081517693', '2025-05-04', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '061191848', '2025-07-26', '2025-04-09');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '021409567', '2025-05-15', '2024-12-25');
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('UPS', '1Z999AA10123456784', '2025-12-06', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '1Z999AA10123456785', '2025-11-01', '2025-11-05');
SELECT * FROM Shippings;

-- INSERT ORDERS
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (19, 20, '2025-02-19 07:58:27', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (34, 39, '2025-07-07 17:09:11', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (38, 37, '2025-09-05 12:45:25', 24);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (30, 12, '2025-10-21 04:21:01', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (5, 17, '2024-12-09 15:55:35', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (7, 32, '2025-09-04 11:12:10', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (20, 31, '2025-08-22 12:31:24', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (13, 34, '2025-07-31 05:58:32', 1);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (10, 5, '2025-08-19 19:01:50', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (31, 27, '2025-01-12 11:46:27', 24);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (27, 22, '2025-11-01 02:09:36', 39);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (28, 27, '2025-06-13 20:56:44', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (21, 25, '2025-11-18 07:55:06', 36);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (37, 9, '2025-10-10 02:14:04', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (18, 8, '2025-08-31 22:18:28', 7);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (9, 23, '2025-03-18 04:06:18', 10);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (6, 14, '2025-10-27 13:04:25', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (32, 33, '2025-10-19 23:00:27', 31);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (18, 28, '2025-02-12 21:37:36', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (38, 31, '2025-06-10 16:54:11', 20);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (28, 14, '2025-04-30 12:25:51', 26);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (24, 13, '2025-08-29 08:27:20', 10);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (36, 38, '2025-01-24 00:21:47', 30);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (35, 19, '2025-08-04 07:59:49', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (26, 19, '2025-04-30 10:02:05', 15);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (10, 7, '2025-07-29 21:25:15', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (22, 36, '2025-02-18 14:42:53', 16);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (9, 24, '2025-03-02 11:48:24', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (17, 15, '2025-09-29 09:33:08', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (31, 16, '2024-12-26 04:54:04', 25);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (8, 33, '2025-07-22 17:57:32', 9);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (33, 5, '2025-08-05 09:47:41', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (8, 35, '2025-03-12 10:35:51', 30);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (22, 36, '2025-01-28 14:50:15', 10);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (12, 14, '2025-09-22 03:09:00', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (32, 30, '2025-07-30 17:27:00', 4);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (23, 19, '2024-12-15 01:58:36', 25);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (23, 16, '2025-01-04 22:53:58', 37);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (3, 37, '2025-09-10 06:51:50', 28);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (24, 30, '2025-09-27 08:18:22', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (10, 3, '2025-04-01 10:30:00', 1);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (12, 8, '2025-12-07 14:20:00', null);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (15, 8, '2025-12-05 10:00:00', 41);
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingId) values (12, 8, '2025-10-28 09:00:00', 42);
SELECT * FROM Orders;

-- Add OrderItems for the delivered order (OrderID 40, assuming 39 orders exist)
insert into OrderItems (OrderID, ItemID) values (40, 10);

-- INSERT ORDER ITEMS
insert into OrderItems (OrderID, ItemID) values (41, 11);
insert into OrderItems (OrderID, ItemID) values (42, 14);
insert into OrderItems (OrderID, ItemID) values (43, 44);
insert into OrderItems (OrderID, ItemID) values (1, 1);
insert into OrderItems (OrderID, ItemID) values (2, 2);
insert into OrderItems (OrderID, ItemID) values (3, 3);
insert into OrderItems (OrderID, ItemID) values (4, 4);
insert into OrderItems (OrderID, ItemID) values (5, 5);
insert into OrderItems (OrderID, ItemID) values (6, 6);
insert into OrderItems (OrderID, ItemID) values (7, 7);
insert into OrderItems (OrderID, ItemID) values (8, 8);
insert into OrderItems (OrderID, ItemID) values (9, 9);
insert into OrderItems (OrderID, ItemID) values (10, 10);
insert into OrderItems (OrderID, ItemID) values (11, 11);
insert into OrderItems (OrderID, ItemID) values (12, 12);
insert into OrderItems (OrderID, ItemID) values (13, 13);
insert into OrderItems (OrderID, ItemID) values (14, 14);
insert into OrderItems (OrderID, ItemID) values (15, 15);
insert into OrderItems (OrderID, ItemID) values (16, 16);
insert into OrderItems (OrderID, ItemID) values (17, 17);
insert into OrderItems (OrderID, ItemID) values (18, 18);
insert into OrderItems (OrderID, ItemID) values (19, 19);
insert into OrderItems (OrderID, ItemID) values (20, 20);
insert into OrderItems (OrderID, ItemID) values (21, 21);
insert into OrderItems (OrderID, ItemID) values (22, 22);
insert into OrderItems (OrderID, ItemID) values (23, 23);
insert into OrderItems (OrderID, ItemID) values (24, 24);
insert into OrderItems (OrderID, ItemID) values (25, 25);
insert into OrderItems (OrderID, ItemID) values (26, 26);
insert into OrderItems (OrderID, ItemID) values (27, 27);
insert into OrderItems (OrderID, ItemID) values (28, 28);
insert into OrderItems (OrderID, ItemID) values (29, 29);
insert into OrderItems (OrderID, ItemID) values (30, 30);
SELECT * FROM OrderItems;

-- INSERT FEEDBACK
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (11, 3, 'Not bad', '2025-05-16 06:31:13', 8);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (10, 5, 'Seller was very understanding and offered a refund', '2025-03-24 04:15:44', 31);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (6, 1, 'but still cute', '2024-12-22 06:05:15', 23);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (4, 1, 'need a replacement', '2025-01-17 09:48:26', 22);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (2, 3, 'need a replacement', '2025-03-09 18:56:52', 28);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (19, 4, 'exceeded my expectations!', '2024-12-05 18:08:46', 12);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (7, 5, 'Packaging was damaged during shipping', '2025-07-01 16:00:07', 35);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (4, 1, 'Item was exactly what I was looking for', '2025-06-13 14:03:55', 31);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (20, 2, 'Exactly what I was looking for', '2025-07-25 01:05:25', 22);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (14, 5, 'Item was exactly as pictured', '2025-04-09 17:37:49', 33);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (20, 2, 'very impressed', '2025-02-15 07:48:49', 20);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (11, 3, 'Item was exactly what I was looking for', '2025-08-15 22:32:51', 35);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (15, 2, 'very satisfied', '2025-06-21 18:40:59', 5);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (10, 1, 'not what I was expecting', '2025-03-25 18:14:51', 25);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (11, 2, 'pleasantly surprised', '2024-12-09 11:18:54', 34);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (14, 5, 'Item was damaged during shipping', '2024-12-29 07:09:14', 13);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (1, 2, 'Product was better than I expected', '2025-10-23 22:50:01', 19);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (16, 5, 'Item arrived damaged', '2025-08-08 03:47:13', 10);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (11, 5, 'A bit disappointed', '2025-03-21 05:48:31', 14);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (7, 1, 'very happy with my purchase', '2025-02-08 05:52:32', 26);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (12, 1, 'but could be better', '2025-05-08 03:20:49', 34);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (5, 1, 'misleading information', '2025-07-03 23:47:02', 31);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (7, 4, 'Seller was very helpful and responsive', '2024-12-17 09:04:44', 12);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (17, 2, 'Product was better than I expected', '2025-12-01 03:14:15', 6);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (1, 2, 'disappointed', '2025-11-15 18:34:48', 18);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (3, 5, 'Item was exactly as pictured', '2025-03-25 02:26:45', 39);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (6, 1, 'Item was exactly as pictured', '2025-01-20 17:41:02', 8);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (17, 1, 'Fast shipping', '2025-08-31 23:08:11', 29);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (8, 2, 'Item was exactly as pictured', '2025-03-02 01:58:08', 36);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (17, 2, 'disappointed', '2025-01-20 20:35:37', 17);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (9, 3, 'but still decent', '2025-09-23 22:07:39', 26);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (16, 4, 'Shipping took longer than expected', '2024-12-03 10:38:45', 26);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (12, 4, 'Quality could be improved', '2025-10-28 06:14:09', 14);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (20, 3, 'Product was better than I expected', '2025-07-05 02:16:36', 19);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (3, 3, 'Overall satisfied with my order', '2025-01-09 07:54:44', 39);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (3, 2, 'Item was damaged during shipping', '2025-02-04 19:37:01', 6);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (3, 3, 'but still usable', '2025-05-04 00:34:26', 30);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (19, 3, 'but it''ll do', '2025-10-18 09:49:28', 25);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (18, 5, 'but still cute', '2025-01-10 19:13:27', 22);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (8, 1, 'Item was damaged during shipping', '2025-11-17 14:31:04', 32);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (4, 3, 'Would buy from this seller again', '2025-04-13 18:58:20', 11);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (2, 3, 'Quality could be improved', '2025-10-24 04:22:30', 39);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (20, 5, 'Great product', '2025-08-26 12:18:02', 19);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (1, 3, 'Fast shipping', '2025-03-19 13:32:25', 29);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (2, 2, 'Exactly what I was looking for', '2025-05-13 06:56:13', 13);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (8, 3, 'very happy with my purchase', '2025-07-14 11:05:05', 34);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (19, 1, 'but it''ll do', '2025-08-05 11:52:33', 22);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (2, 1, 'disappointing', '2025-04-25 12:30:43', 11);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (7, 4, 'Overall satisfied with my order', '2025-01-12 02:18:06', 32);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (17, 2, 'but could be better', '2025-01-05 16:37:40', 34);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (8, 2, 'Item was missing a piece', '2025-06-22 18:05:42', 18);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (17, 5, 'Fast shipping', '2025-11-28 11:37:06', 8);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (4, 1, 'Good value for the price', '2025-08-16 07:22:41', 32);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (4, 2, 'but still nice', '2025-09-21 23:26:17', 5);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (10, 4, 'Item looks different from the photos', '2024-12-21 02:06:10', 6);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (19, 4, 'Seller was friendly and easy to work with', '2025-01-18 02:06:14', 22);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (2, 5, 'Item was damaged during shipping', '2025-10-20 15:01:40', 20);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (18, 2, 'Exactly as described', '2025-05-13 08:50:44', 21);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (18, 2, 'exceeded my expectations!', '2025-11-27 03:42:19', 28);
insert into Feedback (OrderID, Rating, Comment, CreatedAt, CreatedByID) values (15, 2, 'great customer service', '2025-01-07 18:42:59', 11);
SELECT * FROM Feedback;

-- ===========================================================================
-- MINIMAL MOCK SWAP DATA FOR USER 5 (Swapper)
-- ===========================================================================

-- Swap items for user 5 and other users
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Denim Jacket', 'jacket', 'Classic vintage denim jacket', 'M', 'Excellent', false, 5, '2024-01-10 10:00:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Leather Boots', 'shoes', 'Genuine leather boots, barely worn', '9', 'Very good', false, 6, '2024-01-10 11:00:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Cotton T-Shirt', 't-shirt', 'Comfortable cotton t-shirt', 'L', 'Good', false, 5, '2024-01-08 14:00:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Wool Sweater', 'sweater', 'Warm wool sweater for winter', 'M', 'Excellent', false, 8, '2024-01-08 15:00:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Blue Jeans', 'jeans', 'Classic blue jeans, well-maintained', '32', 'Very good', false, 5, '2024-01-05 09:00:00', 'swap');
insert into Items (Title, Category, Description, Size, `Condition`, IsAvailable, OwnerID, ListedAt, `Type`) values ('Silk Blouse', 'blouse', 'Elegant silk blouse for formal occasions', 'S', 'Excellent', false, 10, '2024-01-05 10:00:00', 'swap');

-- Add tags for swap items
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Denim Jacket' AND i.OwnerID = 5 AND t.Title = 'Retro' GROUP BY i.ItemID;
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Denim Jacket' AND i.OwnerID = 5 AND t.Title = 'Urban' GROUP BY i.ItemID;
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Leather Boots' AND i.OwnerID = 6 AND t.Title = 'Edgy' GROUP BY i.ItemID;
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Cotton T-Shirt' AND i.OwnerID = 5 AND t.Title = 'Minimalist' GROUP BY i.ItemID;
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Wool Sweater' AND i.OwnerID = 8 AND t.Title = 'Preppy' GROUP BY i.ItemID;
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Blue Jeans' AND i.OwnerID = 5 AND t.Title = 'Urban' GROUP BY i.ItemID;
insert IGNORE into ItemTags (ItemID, TagID) SELECT DISTINCT i.ItemID, MIN(t.TagID) FROM Items i, Tags t WHERE i.Title = 'Silk Blouse' AND i.OwnerID = 10 AND t.Title = 'Sophisticated' GROUP BY i.ItemID;

-- Shipping records
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('USPS', '9400111899223197428490', '2024-01-12', null);
insert into Shippings (Carrier, TrackingNum, DateShipped, DateArrived) values ('FedEx', '1234567890123', '2024-01-07', '2024-01-09');

-- Pending swap: User 5 giving Denim Jacket, receiving Leather Boots from User 6
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingID) values (5, 6, '2024-01-15 10:30:00', null);
insert into OrderItems (OrderID, ItemID) SELECT o.OrderID, i.ItemID FROM Orders o, Items i WHERE o.GivenByID = 5 AND o.ReceiverID = 6 AND o.CreatedAt = '2024-01-15 10:30:00' AND i.Title = 'Denim Jacket' AND i.OwnerID = 5;
insert into OrderItems (OrderID, ItemID) SELECT o.OrderID, i.ItemID FROM Orders o, Items i WHERE o.GivenByID = 5 AND o.ReceiverID = 6 AND o.CreatedAt = '2024-01-15 10:30:00' AND i.Title = 'Leather Boots' AND i.OwnerID = 6;

-- In Transit swap: User 8 giving Wool Sweater, receiving Cotton T-Shirt from User 5
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingID) SELECT 8, 5, '2024-01-10 14:20:00', s.ShippingID FROM Shippings s WHERE s.TrackingNum = '9400111899223197428490' LIMIT 1;
insert into OrderItems (OrderID, ItemID) SELECT o.OrderID, i.ItemID FROM Orders o, Items i WHERE o.GivenByID = 8 AND o.ReceiverID = 5 AND o.CreatedAt = '2024-01-10 14:20:00' AND i.Title = 'Wool Sweater' AND i.OwnerID = 8;
insert into OrderItems (OrderID, ItemID) SELECT o.OrderID, i.ItemID FROM Orders o, Items i WHERE o.GivenByID = 8 AND o.ReceiverID = 5 AND o.CreatedAt = '2024-01-10 14:20:00' AND i.Title = 'Cotton T-Shirt' AND i.OwnerID = 5;

-- Delivered swap: User 5 giving Blue Jeans, receiving Silk Blouse from User 10
insert into Orders (GivenByID, ReceiverID, CreatedAt, ShippingID) SELECT 5, 10, '2024-01-05 09:15:00', s.ShippingID FROM Shippings s WHERE s.TrackingNum = '1234567890123' LIMIT 1;
insert into OrderItems (OrderID, ItemID) SELECT o.OrderID, i.ItemID FROM Orders o, Items i WHERE o.GivenByID = 5 AND o.ReceiverID = 10 AND o.CreatedAt = '2024-01-05 09:15:00' AND i.Title = 'Blue Jeans' AND i.OwnerID = 5;
insert into OrderItems (OrderID, ItemID) SELECT o.OrderID, i.ItemID FROM Orders o, Items i WHERE o.GivenByID = 5 AND o.ReceiverID = 10 AND o.CreatedAt = '2024-01-05 09:15:00' AND i.Title = 'Silk Blouse' AND i.OwnerID = 10;