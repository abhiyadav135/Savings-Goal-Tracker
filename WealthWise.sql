-- Active: 1728076097326@@127.0.0.1@3306
create DATABASE WealthWise;
use WealthWise;
create table user(
    U_ID INT PRIMARY KEY,
    U_Name varchar(100),
    U_Password varchar(100)
);
create table goals(
    G_ID int primary key,
    G_Name varchar(100),
    Amount float
);
alter table user drop column U_Name;
alter table goals add column G_Date varchar(100);
select * from goals;
alter table user add constraint unique (U_ID);
alter table goals add constraint unique (G_ID);