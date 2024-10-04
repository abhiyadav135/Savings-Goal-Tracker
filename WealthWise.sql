-- Active: 1728074324625@@127.0.0.1@3306@wealthwise
create DATABASE WealthWise;
use WealthWise;
create table user(
    U_ID INT PRIMARY KEY,
    U_Name varchar(100),
    U_Password varchar(100)
);
create table goals(
    G_ID int primary key,
    U_ID int,
    G_Name varchar(100),
    Amount float,
    FOREIGN KEY (U_ID) REFERENCES user(U_ID)
);
alter table user drop column U_Name;
alter table goals add column G_Date varchar(100);
select * from goals;
alter table user add constraint unique (U_ID);
alter table goals add constraint unique (G_ID);
select * from  user;