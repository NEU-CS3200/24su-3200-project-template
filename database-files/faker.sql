USE campusPerks_db;
INSERT INTO location (locationId, streetAddress, city, state, country, zipcode)
VALUES
(1, '15 Fruit St', 'San Francisco', 'Massachusetts', 'USA', '02110'),
(2, '15 Fruit St', 'San Francisco', 'Illinois', 'USA', '02110'),
(3, '15 Fruit St', 'New York', 'New York', 'USA', '11111'),
(4, '12 Summit Pl', 'Miami', 'California', 'USA', '77777'),
(5, '15 Fruit St', 'Boston', 'California', 'USA', '01950');
INSERT INTO college (collegeName, locationId, noOfStores, noOfUsers, domain)
VALUES
('Northwestern', 4, 0, 0, '@Northwestern.edu'),
('Northeastern', 5, 0, 0, '@Northeastern.edu'),
('UCBerkeley', 3, 0, 0, '@UCBerkeley.edu'),
('Fordham', 1, 0, 0, '@Fordham.edu'),
('UMiami', 1, 0, 0, '@UMiami.edu');
INSERT INTO store (storeId, name, locationId, priceRange, noOfDiscounts, hoursOfOperations, category, phoneNo, website, starRating, delivery, ageRestricted, totalSales, noOfOrders, college, clubId)
VALUES
(1, 'Wollastons', 5, '$$$', 0, '10:00am-5:00pm', 'clothing', '882.664.0395', 'parker.biz', 1, 0, 0, 13277, 47, 'UCBerkeley', NULL),
(2, 'Aroma Joes', 1, '$$$', 0, '11:00am-11:00pm', 'convenience', '8047451749', 'alexander-alvarez.info', 1, 0, 0, 3207, 81, 'UMiami', NULL),
(3, 'Star Market', 2, '$', 0, '10:00am-5:00pm', 'grocery', '+1-583-771-3698', 'sandoval-anderson.com', 3, 1, 0, 5003, 248, 'Northeastern', NULL),
(4, 'Panera', 5, '$$', 0, '12:00pm-9:00pm', 'grocery', '001-234-255-9391x3831', 'taylor-bailey.com', 4, 1, 1, 18902, 444, 'UMiami', NULL),
(5, 'Wollastons', 2, '$$$', 0, '7:00am-12:00am', 'clothing', '412-860-3707x648', 'perez.com', 4, 0, 0, 18453, 219, 'Northeastern', NULL);
INSERT INTO club (clubId, name, college, storeId, numberOfUsers)
VALUES
(1, 'Film Club', 'UCBerkeley', NULL, 0),
(2, 'Badminton Club', 'Northeastern', NULL, 0),
(3, 'Society of Women in Tech', 'Fordham', NULL, 0),
(4, 'Trivia Club', 'UMiami', NULL, 0),
(5, 'Phi Delta Theta', 'Northwestern', NULL, 0);
INSERT INTO discount (discountId, storeId, code, percentOff, item, startDate, endDate, ageRestricted, minPurchase, bdayDiscount)
VALUES
(1, 4, 'REDEEMCODE', 87, 'produce', '2025-04-14', '2025-04-15', 1, 94, 0),
(2, 4, 'SPRINGSALE', 8, 'books', '2025-03-20', '2025-05-05', 1, 13, 0),
(3, 4, 'SALECODE', 32, 'books', '2025-03-30', '2025-05-10', 0, 65, 0),
(4, 3, 'REDEEMCODE', 22, 'coffee', '2025-03-30', '2025-06-01', 1, 84, 1),
(5, 5, 'REDEEMCODE', 88, 'produce', '2025-04-14', '2025-05-05', 1, 23, 1),
(6, 1, 'SPRINGSALE', 22, 'books', '2025-04-14', '2025-04-15', 1, 34, 0),
(7, 3, 'SALECODE', 27, 'furniature', '2025-03-30', '2025-05-10', 0, 50, 1),
(8, 1, 'REDEEMCODE', 10, 'coffee', '2025-02-18', '2025-04-15', 0, 50, 0),
(9, 1, 'BUYBUYBUY', 25, 'clothing', '2025-04-14', '2025-05-05', 1, 21, 1),
(10, 5, 'BUYBUYBUY', 43, 'books', '2025-02-18', '2025-05-05', 1, 28, 1);
INSERT INTO user (username, firstName, lastName, password, college, email, phoneNo, birthdate, age, discountsUsed, clubId)
VALUES
('MeaganGay64', 'Meagan', 'Gay', '&3Nsh((l', 'UCBerkeley', 'MeaganGay64@UCBerkeley.edu', '616-542-6069', '1999-09-12', 23, 0, 5),
('KarenWalker95', 'Karen', 'Walker', 'PV+Qi7Bs', 'Fordham', 'KarenWalker95@Fordham.edu', '462-220-1324x2396', '1999-09-12', 21, 0, 3),
('KellyRobles135', 'Kelly', 'Robles', '_6Iv$Q6P', 'UMiami', 'KellyRobles135@UMiami.edu', '001-631-760-2178x0850', '2002-06-01', 19, 1, 4),
('ArielAyala34', 'Ariel', 'Ayala', 'Tg__4zBm', 'UMiami', 'ArielAyala34@UMiami.edu', '+1-994-640-8526x686', '2003-05-10', 30, 4, 2),
('PaulJohnson36', 'Paul', 'Johnson', 'N@U3Yuz)', 'UMiami', 'PaulJohnson36@UMiami.edu', '767-240-1769x5113', '2005-11-11', 19, 0, 2),
('LoganJones71', 'Logan', 'Jones', '*V0XeRCf', 'Northwestern', 'LoganJones71@Northwestern.edu', '382-746-8596', '2002-06-01', 19, 1, 5),
('TaylorContreras86', 'Taylor', 'Contreras', '$cS4Bya1', 'Northwestern', 'TaylorContreras86@Northwestern.edu', '2267857394', '2001-05-05', 18, 3, 2),
('SheliaArmstrong94', 'Shelia', 'Armstrong', '^a9VBb4t', 'UMiami', 'SheliaArmstrong94@UMiami.edu', '822-893-9440', '2001-05-05', 30, 5, 5),
('TammyHowell76', 'Tammy', 'Howell', 'E)uN65Nf', 'UCBerkeley', 'TammyHowell76@UCBerkeley.edu', '3115198345', '2003-05-10', 21, 2, 3),
('FrankMorton31', 'Frank', 'Morton', 'Q_1!BgOf', 'UMiami', 'FrankMorton31@UMiami.edu', '001-634-425-4856', '2005-11-11', 30, 0, 5);
INSERT INTO discount_used (username, discountId)
VALUES
('FrankMorton31', 3),
('SheliaArmstrong94', 4),
('LoganJones71', 7),
('TaylorContreras86', 3),
('MeaganGay64', 3),
('PaulJohnson36', 7),
('KellyRobles135', 9),
('FrankMorton31', 2),
('TammyHowell76', 5),
('FrankMorton31', 4);
INSERT INTO admin (username, firstName, lastName, password, email, phoneNo, supportUser, supportClub, supportStore)
VALUES
('ValerieMolina53', 'Valerie', 'Molina', 'RO@C4Exa', 'ValerieMolina53@gmail.com', '718-870-6829x0832', 'KellyRobles135', 5, 4),
('DavidZavala56', 'David', 'Zavala', 'B&5&6Qte', 'DavidZavala56@gmail.com', '+1-345-708-5215x714', 'LoganJones71', 3, 2);