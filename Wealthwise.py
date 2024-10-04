from flask import Flask,request,render_template
import mysql.connector

# Establishing the connection
cnx=mysql.connector.connect(
    user='username'
    password='password'
    host='127.0.0.1')

# Creating a cursor
cur=cnx.cursor()


app=Flask(_name_)

@app.route('/')
def index():
    return render_template('index.html')
