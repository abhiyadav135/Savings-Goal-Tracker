from flask import Flask, redirect,request,render_template, url_for
import mysql.connector

# Configuration
DB_USER = 'root'
DB_PASSWORD = 'up80t5011'
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


app=Flask(__name__)

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
            break
        # Redirect to goal setup page
        return redirect(url_for('setup_goal', u_id=u_id))
    
    return render_template('new-member.html')

@app.route('/setup-goal', methods=['GET', 'POST'])
def setup_goal():

    u_id = request.args.get('u_id')
    if request.method == 'POST':
        g_name = request.form['goal_name']
        g_amount = float(request.form['goal_amount'])
        g_date = request.form['goal_date']
        
        cur.execute("INSERT INTO goals (G_ID, G_Name, Amount, G_Date) VALUES (%s, %s, %s, %s)",
                     (u_id, g_name, g_amount, g_date))
        cnx.commit()
        
        return "Goal setup successfully!"
    
    return render_template('setup-goal.html')