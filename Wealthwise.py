from flask import Flask,request,render_template
import mysql.connector

# Configuration
DB_USER = 'root'
DB_PASSWORD = 'GAnDCfvtKpAE?F*mBmKbu:%*JAeC4!T$)c8mxqmPstsC;=vqpnd^qk4ZCBX1qe$q'
DB_HOST = '127.0.0.1'
DB_NAME = 'mydatabase'


# Establishing the connection
cnx = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

# Creating a cursor
cur=cnx.cursor()


app=Flask(_name_)

@app.route('/existing-member')
def existing():
    current_route = request.path
    if current_route == '/existing-member':
        print("Existing member page is opened")
        
    return render_template('existing-member.html')


@app.route('/new-member', methods=['GET', 'POST'])
def new_member():
    if request.method == 'POST':
        u_id = request.form['uid']
        u_password = request.form['upassword']
        u_confirm_password = request.form['uconfirmpassword']
    while True:
        if u_password == u_confirm_password:
            cur.execute("INSERT INTO user (U_ID,U_Password) VALUES (%s, %s)",
                         (u_id, u_password))
            cnx.commit()
            return "User  created successfully!"
            break
    return render_template('new-member.html')

