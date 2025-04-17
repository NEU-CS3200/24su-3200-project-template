USE campusPerks_db;
INSERT INTO location (locationId, streetAddress, city, state, country, zipcode)
VALUES
(1, '12 Summit Pl', 'Miami', 'Florida', 'USA', '02110'),
(2, '12 Summit Pl', 'Boston', 'New York', 'USA', '11111'),
(3, '14 Baker St', 'Boston', 'New York', 'USA', '77777'),
(4, '199 High St', 'San Francisco', 'California', 'USA', '90210'),
(5, '14 Baker St', 'Boston', 'Florida', 'USA', '77777');
INSERT INTO college (collegeName, locationId, noOfStores, noOfUsers, domain)
VALUES
('Northeastern', 3, 0, 0, '@Northeastern.edu'),
('UMiami', 4, 0, 0, '@UMiami.edu'),
('Northwestern', 5, 0, 0, '@Northwestern.edu'),
('UCBerkeley', 2, 0, 0, '@UCBerkeley.edu'),
('Fordham', 1, 0, 0, '@Fordham.edu');
INSERT INTO store (storeId, name, locationId, priceRange, noOfDiscounts, hoursOfOperations, category, phoneNo, website, starRating, delivery, ageRestricted, totalSales, noOfOrders, college, clubId)
VALUES
(1, 'Target', 1, '$', 0, '11:00am-11:00pm', 'grocery', '(697)547-7537x5922', 'garcia.com', 2, 0, 0, 17154, 411, 'Fordham', NULL),
(2, 'Target', 1, '$$$', 0, '10:00am-5:00pm', 'food', '001-554-410-5227x706', 'jimenez.biz', 5, 0, 0, 1158, 148, 'Northeastern', NULL),
(3, 'Star Market', 4, '$$$', 0, '10:00am-5:00pm', 'food', '(543)965-5854x8895', 'williams.com', 3, 1, 1, 13173, 79, 'Northeastern', NULL),
(4, 'Aroma Joes', 1, '$$$', 0, '7:00am-12:00am', 'grocery', '(685)393-7427', 'garcia.biz', 5, 0, 1, 9908, 319, 'Northwestern', NULL),
(5, 'Target', 2, '$$', 0, '12:00pm-9:00pm', 'food', '240.433.1056x67917', 'wilson.com', 4, 0, 0, 15949, 242, 'UCBerkeley', NULL);
INSERT INTO club (clubId, name, college, storeId, numberOfUsers)
VALUES
(1, 'Society of Women in Tech', 'Northeastern', NULL, 0),
(2, 'Film Club', 'Fordham', NULL, 0),
(3, 'Trivia Club', 'UMiami', NULL, 0),
(4, 'Film Club', 'Northwestern', NULL, 0),
(5, 'Film Club', 'UCBerkeley', NULL, 0);
INSERT INTO discount (discountId, storeId, code, percentOff, item, startDate, endDate, ageRestricted, minPurchase, bdayDiscount)
VALUES
(1, 5, 'REDEEMCODE', 64, 'books', '2025-02-18', '2025-05-05', 1, 80, 0),
(2, 1, 'REDEEMCODE', 68, 'coffee', '2025-03-20', '2025-06-01', 1, 55, 1),
(3, 5, 'BUYBUYBUY', 57, 'books', '2025-04-14', '2025-04-15', 1, 86, 1),
(4, 5, 'SPRINGSALE', 13, 'books', '2025-03-20', '2025-04-15', 0, 36, 0),
(5, 4, 'BUYBUYBUY', 11, 'coffee', '2025-03-20', '2025-05-10', 0, 31, 0),
(6, 4, 'SALECODE', 38, 'clothing', '2025-03-20', '2025-05-10', 0, 73, 1),
(7, 4, 'SPRINGSALE', 39, 'coffee', '2025-03-20', '2025-04-15', 1, 52, 1),
(8, 5, 'SALECODE', 13, 'produce', '2025-03-20', '2025-05-10', 1, 63, 1),
(9, 3, 'SPRINGSALE', 94, 'clothing', '2025-03-20', '2025-05-05', 0, 55, 0),
(10, 4, 'BIGSALE', 69, 'clothing', '2025-04-14', '2025-04-15', 0, 73, 0);
INSERT INTO user (username, firstName, lastName, password, college, email, phoneNo, birthdate, age, discountsUsed, clubId)
VALUES
('MelindaAnderson51', 'Melinda', 'Anderson', '&q87EszT', 'Fordham', 'MelindaAnderson51@Fordham.edu', '590.347.5148x740', '2005-11-11', 18, 2, 1),
('NicoleWilliams87', 'Nicole', 'Williams', '*Y_0VrsK', 'UCBerkeley', 'NicoleWilliams87@UCBerkeley.edu', '(287)855-7884x6357', '2001-05-05', 21, 0, 5),
('RickyDouglas126', 'Ricky', 'Douglas', 'h%7eA5Wp', 'Northeastern', 'RickyDouglas126@Northeastern.edu', '+1-730-995-7367x8489', '2001-05-05', 18, 1, 4),
('NicoleSullivan99', 'Nicole', 'Sullivan', 'dy!fQ5Dh', 'Northeastern', 'NicoleSullivan99@Northeastern.edu', '(599)307-5704', '1999-09-12', 24, 2, 1),
('AlexanderChavez136', 'Alexander', 'Chavez', 'KU+r9cFs', 'Northwestern', 'AlexanderChavez136@Northwestern.edu', '+1-696-789-7737x71613', '2001-05-05', 23, 5, 5),
('DavidPowers73', 'David', 'Powers', 'vRB^5yLy', 'Northwestern', 'DavidPowers73@Northwestern.edu', '7237349118', '2002-06-01', 20, 0, 4),
('DianeBriggs160', 'Diane', 'Briggs', '#5MZNnKJ', 'UCBerkeley', 'DianeBriggs160@UCBerkeley.edu', '261.416.8686', '2005-11-11', 26, 1, 5),
('RonaldLogan186', 'Ronald', 'Logan', '0&0tHpTg', 'Fordham', 'RonaldLogan186@Fordham.edu', '+1-372-245-6260x76430', '2003-05-10', 24, 5, 5),
('ColinJones40', 'Colin', 'Jones', '#8D*FXHd', 'Fordham', 'ColinJones40@Fordham.edu', '001-252-380-4114', '2000-04-15', 30, 2, 3),
('RicardoPreston96', 'Ricardo', 'Preston', '#1VOubw9', 'Northwestern', 'RicardoPreston96@Northwestern.edu', '238-380-7029x8390', '2003-05-10', 21, 2, 2);
INSERT INTO discount_used (username, discountId)
VALUES
('NicoleWilliams87', 8),
('NicoleWilliams87', 7),
('NicoleSullivan99', 6),
('RonaldLogan186', 10),
('AlexanderChavez136', 9),
('RickyDouglas126', 5),
('AlexanderChavez136', 5),
('ColinJones40', 1),
('AlexanderChavez136', 2),
('ColinJones40', 4);
INSERT INTO admin (username, firstName, lastName, password, email, phoneNo, supportUser, supportClub, supportStore)
VALUES
('VictorGreen126', 'Victor', 'Green', ')!+4Yg0y', 'VictorGreen126@gmail.com', '(392)519-1191x748', 'ColinJones40', 5, 5),
('MarkOrtega104', 'Mark', 'Ortega', '(9O%7v!s', 'MarkOrtega104@gmail.com', '716.293.7517', 'NicoleWilliams87', 3, 3);
