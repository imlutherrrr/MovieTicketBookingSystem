create database movie_ticket_booking;
use movie_ticket_booking;

create table location(
location_id int auto_increment primary key,
location_name varchar(255) not null
);

create table theatre(
theatre_id int auto_increment primary key,
name varchar(255) not null,
picture varchar(255) not null,
address varchar(255) not null,
location_id int not null,
foreign key(location_id) references location(location_id)
);

create table screen(
screen_id int auto_increment primary key,
number_of_seats int not null,
screen_size varchar(255) not null,
sound varchar(255) not null,
theatre_id int not null,
screen_title varchar(255) not null,
foreign key(theatre_id) references theatre(theatre_id)
);

create table timings(
timings_id int auto_increment primary key,
screen_id int not null,
show_time time not null,
foreign key(screen_id) references screen(screen_id)
);

create table movies(
movies_id int auto_increment primary key,
movie_name varchar(255) not null,
picture varchar(255) not null,
duration varchar(255) not null,
genre varchar(255) not null,
description varchar(255) not null,
status varchar(255) not null,
release_date date not null
);

create table now_showing(
now_showing_id int auto_increment primary key,
from_date date not null,
to_date date not null,
screen_id int not null,
movies_id int not null,
ticket_price int not null,
foreign key(screen_id) references screen(screen_id),
foreign key(movies_id) references movies(movies_id)
);

create table user(
user_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null,
phone varchar(255) not null,
password varchar(255) not null
);

create table booking(
booking_id int auto_increment primary key,
user_id int not null,
timings_id int not null,
status varchar(255) not null,
booking_date varchar(255) not null,
number_of_seats int not null,
now_showing_id int not null,
date datetime default current_timestamp,
amount int not null,
foreign key(user_id) references user(user_id),
foreign key(timings_id) references timings(timings_id),
foreign key(now_showing_id) references now_showing(now_showing_id)
);


create table payment(
payment_id int auto_increment primary key,
booking_id int not null,
card_number varchar(255) not null,
card_holder_name varchar(255) not null,
cvv varchar(255) not null,
expiry_date varchar(255) not null,
date datetime default current_timestamp,
foreign key(booking_id) references booking(booking_id)
);

create table booked_seats(
booked_seats_id int auto_increment primary key,
booking_id int not null,
seat_numbers int not null,
status varchar(255) not null,
foreign key(booking_id) references booking(booking_id)
);
