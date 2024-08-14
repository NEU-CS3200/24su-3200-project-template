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