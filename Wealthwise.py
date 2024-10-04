from flask import Flask, flash, redirect,request,render_template, url_for
import mysql.connector

# Configuration
DB_USER = 'root'
DB_PASSWORD = 'up80t5011'
DB_HOST = '127.0.0.1'
DB_NAME = 'WealthWise'


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

@app.route('/existing-member', methods=['GET', 'POST'])
def existing_member():
    if request.method == 'POST':
        u_id = request.form['uid']
        u_password = request.form['upassword']
        
        
        
        # Check if the user exists in the database
        cur.execute("SELECT * FROM user WHERE U_ID = %s AND U_Password = %s", (u_id))
        user_data = cur.fetchone()
        
        if user_data:
            # User exists, show goal amount, goal progress, and transaction history
            cur.execute("SELECT * FROM goals WHERE U_ID = %s", (u_id,))
            goal_data = cur.fetchall()
            
            goal_amount = 0
            remaining_amount = 0
            goal_progress = 0
            
            for goal in goal_data:
                goal_amount += goal[2]
                remaining_amount += goal[2]  # Assuming the remaining amount is the same as the goal amount for now
            
            if goal_amount > 0:
                goal_progress = (goal_amount - remaining_amount) / goal_amount * 100
            
            # Get transaction history
            # You should create a 'transactions' table in your SQL script
            # cur.execute("SELECT * FROM transactions WHERE U_ID = %s", (u_id,))
            # transaction_data = cur.fetchall()
            
            return render_template('existing-member.html', 
                                   u_id=u_id, 
                                   goal_amount=goal_amount, 
                                   goal_progress=goal_progress)
        else:
            flash("Invalid username or password")
            return redirect(url_for('existing_member'))
    
    return render_template('existing-member.html')

@app.route('/new-member', methods=['GET', 'POST'])
def new_member():
    if request.method == 'POST':
        u_id = request.form['uid']
        u_password = request.form['upassword']
        u_confirm_password = request.form['uconfirmpassword']
    while True:
        if u_password == u_confirm_password:
            
            cur.execute("INSERT INTO user (U_ID, U_Password) VALUES (%s, %s)", (u_id))
            cnx.commit()
            return redirect(url_for('setup_goal', u_id=u_id))
        else:
            flash("Passwords do not match")
            return redirect(url_for('new_member'))
    
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