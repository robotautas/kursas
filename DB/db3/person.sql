create table person (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(50),
	car_id INT,
	company_id INT,
	FOREIGN KEY (car_id) REFERENCES car(id),
	FOREIGN KEY (company_id) REFERENCES company(id)
);
insert into person (id, first_name, last_name, email, car_id, company_id) values (1, 'Innis', 'Netley', 'inetley0@cornell.edu', 10, 1);
insert into person (id, first_name, last_name, email, car_id, company_id) values (2, 'Claudetta', 'Dewey', 'cdewey1@mit.edu', 4, 3);
insert into person (id, first_name, last_name, email, car_id, company_id) values (3, 'Carri', 'Sharpus', 'csharpus2@telegraph.co.uk', 3, 4);
insert into person (id, first_name, last_name, email, car_id, company_id) values (4, 'Andras', 'Brownsea', 'abrownsea3@webnode.com', 12, 5);
insert into person (id, first_name, last_name, email, car_id, company_id) values (5, 'Philippe', 'Longhirst', 'plonghirst4@paginegialle.it', 9, 5);
insert into person (id, first_name, last_name, email, car_id, company_id) values (6, 'Lenore', 'Whatson', 'lwhatson5@diigo.com', 11, 4);
insert into person (id, first_name, last_name, email, car_id, company_id) values (7, 'Shelba', 'Gummer', 'sgummer6@devhub.com', 1, 5);
insert into person (id, first_name, last_name, email, car_id, company_id) values (8, 'Nanny', 'Severns', 'nseverns7@cnbc.com', 7, 5);
insert into person (id, first_name, last_name, email, car_id, company_id) values (9, 'Irvine', 'Kenewell', 'ikenewell8@cnn.com', 2, 3);
insert into person (id, first_name, last_name, email, car_id, company_id) values (10, 'Randy', 'Hanscomb', 'rhanscomb9@dagondesign.com', 13, 4);
insert into person (id, first_name, last_name, email, car_id, company_id) values (11, 'Dun', 'Zarfai', 'dzarfaia@istockphoto.com', 5, 5);
insert into person (id, first_name, last_name, email, car_id, company_id) values (12, 'Regan', 'Halliday', 'rhallidayb@mlb.com', 14, 1);
insert into person (id, first_name, last_name, email, car_id, company_id) values (13, 'Abbott', 'Sharphurst', 'asharphurstc@boston.com', null, 1);
insert into person (id, first_name, last_name, email, car_id, company_id) values (14, 'Westbrook', 'Stirtle', 'wstirtled@ustream.tv', 8, 2);
insert into person (id, first_name, last_name, email, car_id, company_id) values (15, 'Drucy', 'Whittles', 'dwhittlese@bbb.org', null, 5);
insert into person (id, first_name, last_name, email, car_id, company_id) values (16, 'Frankie', 'Yaknov', 'fyaknovf@bandcamp.com', 6, 3);
