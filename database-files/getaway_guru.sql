drop database if exists getawayguru;
create database getawayguru;

use getawayguru;

create table if not exists users (
    id integer auto_increment primary key,
    email varchar(255) unique,
    address varchar(255),
    username varchar(255) unique
);

create table if not exists employee (
    id integer auto_increment primary key,
    email varchar(255) unique,
    first_name varchar(255),
    last_name varchar(255)
);

create table if not exists tracks (
    tracked_id integer,
    trackee_id integer,
    primary key (tracked_id, trackee_id),
    constraint fk_1 foreign key (tracked_id) references users (id) on update cascade,
    constraint fk_2 foreign key (trackee_id) references employee (id) on update cascade
);


create table if not exists city (
    id integer auto_increment primary key,
    country varchar(255),
    rating integer,
    name varchar(255)

);

create table if not exists trip (
    id integer auto_increment primary key,
    start_date date,
    end_date date,
    group_size integer,
    name varchar(255),
    restaurant varchar(255),
    budget integer,
    hotel_budget integer,
    flight_budget integer,
    user_id integer unique,
    city_id integer unique,
    attraction_budget integer,
    restaurant_budget integer,
    num_of_nights integer,
    constraint fk_3 foreign key (user_id) references users (id) on update cascade,
    constraint fk_4 foreign key (city_id) references city (id) on update cascade
);


create table if not exists hotel (
    id integer auto_increment primary key,
    room_type varchar(255),
    amenities varchar(255),
    price_per_night integer,
    email varchar(255),
    name varchar(255),
    rating integer,
    city_id integer,
    constraint fk_5 foreign key (city_id) references city(id) on update cascade
);

create table if not exists attraction (
    id integer auto_increment primary key,
    price integer,
    address varchar(255),
    rating integer,
    city_id integer,
    name varchar(255),
    constraint fk_6 foreign key (city_id) references city (id) on update cascade
);


create table if not exists restaurant (
    id integer auto_increment primary key,
    average_price integer,
    address varchar(255),
    rating integer,
    cuisine_type varchar(255),
    city_id integer,
    name varchar(255),
    constraint fk_7 foreign key (city_id) references city (id) on update cascade
);

create table if not exists flights (
    flight_id integer primary key,
    airline_id integer,
    airline_name varchar(255),
    duration integer,
    departure datetime,
    arrival datetime,
    price integer,
    origin_city varchar(255),
    city_id integer,
    constraint fk_8 foreign key(city_id) references city (id) on update cascade

);

create table if not exists marketing_campaign (
    id integer auto_increment primary key,
    name varchar(255),
    employee_id integer,
    constraint fk_9 foreign key (employee_id) references employee (id) on update cascade
);

create table if not exists promotions (
    code integer primary key,
    name varchar(255),
    discount_amount integer,
    terms_and_conditions varchar(255),
    marketing_campaign_id integer,
    constraint fk_10 foreign key (marketing_campaign_id) references marketing_campaign (id) on update cascade
);

create table if not exists ads (
    id integer auto_increment primary key,
    description varchar(255),
    type varchar(255),
    budget integer,
    terms_and_conditions varchar(255),
    marketing_campaign_id integer,
    constraint fk_11 foreign key (marketing_campaign_id) references marketing_campaign (id) on update cascade

);

create table if not exists city_clicks (
    city_id integer,
    city varchar(255),
    city_click_id integer,
    country varchar(255),
    user_id integer,
    clicked_at datetime default current_timestamp,
    primary key (user_id, city_click_id),
    constraint fk_12 foreign key (city_id) references city(id) on update cascade,
    constraint fk_13 foreign key (user_id) references users (id) on update cascade
);


create table if not exists hotel_clicks (
    hotel_id integer,
    click_counter integer,
    country varchar(255),
    hotel_click_id integer,
    user_id integer,
    clicked_at datetime default current_timestamp,
    primary key (user_id, hotel_click_id),
    constraint fk_14 foreign key (hotel_id) references hotel(id) on update cascade,
    constraint fk_15 foreign key (user_id) references users (id) on update cascade
);

create table if not exists attraction_clicks (
    attraction_id integer,
    click_counter integer,
    country varchar(255),
    user_id integer,
    clicked_at datetime default current_timestamp,
    attraction_click_id integer,
    primary key (user_id, attraction_click_id),
    constraint fk_16 foreign key (attraction_id) references attraction(id) on update cascade,
    constraint fk_17 foreign key (user_id) references users (id)  on update cascade
);

create table if not exists restaurant_clicks (
    restaurant_id integer,
    click_counter integer,
    country varchar(255),
    user_id integer,
    clicked_at datetime default current_timestamp,
    restaurant_click_id integer,
    primary key (user_id, restaurant_click_id),
    constraint fk_18 foreign key (restaurant_id) references restaurant(id) on update cascade,
    constraint fk_19 foreign key (user_id) references users (id) on update cascade
);

use getawayguru;
-- Users Table
INSERT INTO users (id, email, address, username)
VALUES (1, 'john.doe@example.com', '123 Main St', 'johndoe');
INSERT INTO users (id, email, address, username)
VALUES (2, 'jane.doe@example.com', '456 Oak St', 'janedoe');


-- Employee Table
INSERT INTO employee (id, email, first_name, last_name)
VALUES (1, 'alice@example.com', 'Alice', 'Smith');
INSERT INTO employee (id, email, first_name, last_name)
VALUES (2, 'bob@example.com', 'Bob', 'Johnson');


-- Tracks Table
INSERT INTO tracks (tracked_id, trackee_id)
VALUES (1, 1);
INSERT INTO tracks (tracked_id, trackee_id)
VALUES (2, 2);


-- City Table
INSERT INTO city (id, country, rating, name)
VALUES (1, 'USA', 4, 'Los Angeles');
INSERT INTO city (id, country, rating, name)
VALUES (2, 'Canada', 5, 'Quebec');


-- Trip Table
INSERT INTO trip (id, start_date, end_date, group_size, name, restaurant, budget, hotel_budget, flight_budget, user_id, city_id, attraction_budget, restaurant_budget, num_of_nights)
VALUES (1, '2024-08-01', '2024-08-07', 4, 'Summer Trip', 'The Grill', 2000, 500, 800, 1, 1, 200, 300, 6);
INSERT INTO trip (id, start_date, end_date, group_size, name, restaurant, budget, hotel_budget, flight_budget, user_id, city_id, attraction_budget, restaurant_budget, num_of_nights)
VALUES (2, '2024-09-01', '2024-09-07', 4, 'Winter Trip', 'The SteakHouse', 4000, 400, 1600, 2, 2, 300, 500, 6);


-- Hotel Table
INSERT INTO hotel (id, room_type, amenities, price_per_night, email, name, rating, city_id)
VALUES (1, 'Suite', 'Pool, Wi-Fi', 1200, 'hotel@example.com', 'Hilton', 5, 1);
INSERT INTO hotel (id, room_type, amenities, price_per_night, email,name, rating, city_id)
VALUES (2, 'Deluxe', 'Wi-Fi, Gym', 900, 'hotel2@example.com','Urban Oasis', 3, 2);


-- Attraction Table
INSERT INTO attraction (id, price, address, rating, city_id, name)
VALUES (1, 50, '123 Park Ave', 4, 1, 'Six Flags');
INSERT INTO attraction (id, price, address, rating, city_id,name)
VALUES (2, 30, '456 Museum Rd', 5, 2, 'Water Park');




-- Restaurant Table
INSERT INTO restaurant (id, average_price, address, rating, cuisine_type, city_id, name)
VALUES (1, 40, '789 Food St', 5, 'Italian', 1, 'Chefs Kiss');
INSERT INTO restaurant (id, average_price, address, rating, cuisine_type, city_id, name)
VALUES (2, 30, '1011 Dine Blvd', 4, 'Mexican', 2, 'Panda Express');


-- Flights Table
INSERT INTO flights (flight_id, airline_id, airline_name, duration, departure, arrival, price, origin_city, city_id)
VALUES (1, 101, 'Airways', 180, '2024-08-01 09:00:00', '2024-08-01 12:00:00', 300, 'New York', 1);
INSERT INTO flights (flight_id, airline_id, airline_name, duration, departure, arrival, price, origin_city, city_id)
VALUES (2, 102, 'Skyline', 240, '2024-08-02 14:00:00', '2024-08-02 18:00:00', 450, 'Los Angeles', 2);


-- Marketing Campaign Table
INSERT INTO marketing_campaign (id, name, employee_id)
VALUES (1, 'Summer Sale', 1);
INSERT INTO marketing_campaign (id, name, employee_id)
VALUES (2, 'Winter Discount', 2);


-- Promotions Table
INSERT INTO promotions (code, name, discount_amount, terms_and_conditions, marketing_campaign_id)
VALUES (101, 'SUMMER2024', 20, 'Valid till Aug 31, 2024', 1);
INSERT INTO promotions (code, name, discount_amount, terms_and_conditions, marketing_campaign_id)
VALUES (102, 'WINTER2024', 25, 'Valid till Dec 31, 2024', 2);


-- Ads Table
INSERT INTO ads (id, description, type, budget, terms_and_conditions, marketing_campaign_id)
VALUES (1, 'Ad for summer sale', 'Banner', 500, 'Terms apply', 1);
INSERT INTO ads (id, description, type, budget, terms_and_conditions, marketing_campaign_id)
VALUES (2, 'Ad for winter discount', 'Video', 1000, 'Terms apply', 2);


-- City Clicks Table
INSERT INTO city_clicks (city_id, city, city_click_id, country, user_id)
VALUES (1, 'New York', 101, 'USA', 1);
INSERT INTO city_clicks (city_id, city, city_click_id, country, user_id)
VALUES (2, 'Los Angeles', 102, 'USA', 2);


-- Hotel Clicks Table
INSERT INTO hotel_clicks (hotel_id, click_counter, country, hotel_click_id, user_id)
VALUES (1, 10, 'USA', 201, 1);
INSERT INTO hotel_clicks (hotel_id, click_counter, country, hotel_click_id, user_id)
VALUES (2, 15, 'USA', 202, 2);


-- Attraction Clicks Table
INSERT INTO attraction_clicks (attraction_id, click_counter, country, user_id, attraction_click_id)
VALUES (1, 20, 'USA', 1, 301);
INSERT INTO attraction_clicks (attraction_id, click_counter, country, user_id, attraction_click_id)
VALUES (2, 25, 'USA', 2, 302);


-- Restaurant Clicks Table
INSERT INTO restaurant_clicks (restaurant_id, click_counter, country, user_id, restaurant_click_id)
VALUES (1, 15, 'USA', 1, 401);
INSERT INTO restaurant_clicks (restaurant_id, click_counter, country, user_id, restaurant_click_id)
VALUES (2, 18, 'USA', 2, 402);


-- 1.1
SELECT price, country AS Possible_Locations
FROM trip JOIN city ON trip.city_id = city.id
JOIN flights ON city.id = flights.city_id
WHERE trip.flight_budget >= flights.price
ORDER BY flights.price ASC;

-- 1.2
UPDATE users
SET address = 'current address'
Where users.id = 1;

-- 1.3
INSERT INTO users(id, email, address, username)
	VALUES(4, 'alice123@gmail.com', 'address', 'alice45');
UPDATE trip
SET hotel_budget = 3000,
    flight_budget = 1200,
    attraction_budget = 5000,
    restaurant_budget = 3000
WHERE id = 4;

-- 2.1
SELECT c.name, u.ID, u.username, cc.clicked_at
FROM users u JOIN city_clicks cc ON u.id = cc.user_id join city c on cc.city_id = c.id
GROUP BY c.name, u.id, u.username, cc.clicked_at
ORDER BY cc.clicked_at ;

-- 2.2
SELECT rating, name
FROM hotel
ORDER BY rating DESC;

SELECT rating, name
FROM restaurant
ORDER BY rating DESC;

-- 2.3
SELECT email, rating
FROM hotel
WHERE rating >= 4
ORDER BY rating DESC;

-- 3.1
SELECT rating, price_per_night, room_type
FROM hotel JOIN trip ON hotel.price_per_night <= (trip.hotel_budget / trip.num_of_nights)
WHERE rating >= 4
ORDER BY price_per_night ASC;

-- 3.2
SELECT rating, cuisine_type, average_price
FROM restaurant
WHERE rating >= 4
ORDER BY average_price DESC;

-- 3.3
SELECT duration, price, flight_budget
FROM trip JOIN city ON trip.city_id = city.id
	        JOIN flights ON flights.city_id = city.id
WHERE duration >= 5
ORDER BY price ASC;
























