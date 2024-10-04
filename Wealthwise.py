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

@app.route('/', methods=['GET'])
def index():
    return render_template('first.html')


@app.route('/existing-member', methods=['GET', 'POST'])
def existing_member():
    if request.method == 'POST':
        u_id = request.form['userId']
        u_password = request.form['password']
        
        
        
        # Check if the user exists in the database
        cur.execute("SELECT * FROM user WHERE U_ID = %s AND U_Password = %s", (u_id,u_password))
        user_data = cur.fetchone()
        
        if user_data:
            # User exists, show goal amount, goal progress, and transaction history
            cur.execute("SELECT * FROM goals WHERE U_ID = %s AND U_Password=%s", (u_id,u_password))
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
        
    
    return render_template('existing-member.html')

@app.route('/new-member', methods=['GET', 'POST'])
def new_member():
    if request.method == 'POST':
        u_id = request.form['userId']
        u_password = request.form['password']
        u_confirm_password = request.form['confirmPassword']

        if u_password == u_confirm_password:
            # Check if the user already exists
            cur.execute("SELECT * FROM user WHERE U_ID = %s", (u_id,))
            user_data = cur.fetchone()

            if user_data:
                flash("User  ID already exists. Please choose a different ID.")
                return render_template('new-member.html'), {'message': 'User  ID already exists. Please choose a different ID.'}

            # Insert the new user into the database
            cur.execute("INSERT INTO user (U_ID, U_Password) VALUES (%s, %s)", (u_id, u_password))
            cnx.commit()
            return redirect(url_for('goals', u_id=u_id))

    return render_template('new-member.html')

@app.route('goals', methods=['GET', 'POST'])
def goals():

    u_id = request.args.get('u_id')
    if request.method == 'POST':
        g_name = request.form['goalName']
        g_amount = float(request.form['goalAmount'])
        g_date = request.form['goalDeadline']
        
        cur.execute("INSERT INTO goals (G_Name, Amount, G_Date) VALUES ( %s, %s, %s)",
                     ( g_name, g_amount, g_date))
        cnx.commit()
        
        return "Goal setup successfully!"
    
    return render_template('goals.html')