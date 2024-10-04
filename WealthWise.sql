-- Active: 1728062483228@@127.0.0.1@3306@WealthWise
use WealthWise;
create table user(
    U_ID INT PRIMARY KEY,
    U_Name varchar(100),
    U_Password varchar(100)
);