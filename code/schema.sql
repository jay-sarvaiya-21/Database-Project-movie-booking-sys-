
drop table if exists  Employee cascade;
drop table if exists  MoviePool cascade;
drop table if exists  ScreeningMovie cascade;

drop table if exists  Seats cascade;
drop table if exists  Users cascade;
drop table if exists  Ticket cascade;


create table Screen (
 Sc_id varchar(32) primary key,
 capacity integer
);

insert into Screen(Sc_id,capacity) values('A1',10);
insert into Screen(Sc_id,capacity) values('A2',15);
insert into Screen(Sc_id,capacity) values('A3',10);
insert into Screen(Sc_id,capacity) values('A4',10);
insert into Screen(Sc_id,capacity) values('A5',9);
insert into Screen(Sc_id,capacity) values('B1',10);
insert into Screen(Sc_id,capacity) values('B2',7);
insert into Screen(Sc_id,capacity) values('B3',8);
insert into Screen(Sc_id,capacity) values('B4',20);
insert into Screen(Sc_id,capacity) values('B5',5);
insert into Screen(Sc_id,capacity) values('C1',9);
insert into Screen(Sc_id,capacity) values('C2',5);
insert into Screen(Sc_id,capacity) values('C3',5);
insert into Screen(Sc_id,capacity) values('C4',5);
insert into Screen(Sc_id,capacity) values('C5',20);
insert into Screen(Sc_id,capacity) values('D1',15);
insert into Screen(Sc_id,capacity) values('D2',10);
insert into Screen(Sc_id,capacity) values('D3',20);
insert into Screen(Sc_id,capacity) values('D4',10);
insert into Screen(Sc_id,capacity) values('D5',10);


		
create table MoviePool (
 Movie_id integer,
 M_name varchar(128),
 Duration integer not null,
 publish date,
 Genre varchar(128),
 primary key (Movie_id, M_name)
);


create table Employee (
 Emp_id integer primary key,
 E_name varchar(32),
 Gender varchar(32),
 contact_no bigint
);


create table Users (
 U_id varchar(32) primary key,
 Name_is varchar(32),
 password_is varchar(128),
 Gender varchar(32),
 Dob date
);


create table ScreeningMovie (
 Scm_id varchar(32) primary key,
 Movie_id integer not null,
 M_name varchar(128) not null ,
 starting time,
 Emp_id integer not null,
 Sc_id varchar(32) not null,
 foreign key (Movie_id, M_name) references MoviePool (Movie_id, M_name),
 foreign key (Emp_id) references Employee (Emp_id),
 foreign key (Sc_id) references Screen (Sc_id)
);


create table Seats (
 Seat_id varchar(32),
 Sc_id varchar(32), 
 price decimal,
 primary key (Seat_id, Sc_id),
 foreign key (Sc_id) references Screen (Sc_id) on delete cascade
);


create table Ticket (
 Ticket_id varchar(32) primary key,
 Seat_id varchar(32) not null,
 Sc_id varchar(32) not null,
 Scm_id varchar(32) not null,
 U_id varchar(32) not null,
 foreign key (Seat_id, Sc_id) references Seats (Seat_id, Sc_id),
 foreign key (U_id) references Users (U_id),
 foreign key (Scm_id) references ScreeningMovie (Scm_id)
);


