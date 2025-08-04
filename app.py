from flask import Flask, render_template, request, redirect, url_for, session 
import bcrypt
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)


@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password'].encode('utf-8')
        email=request.form['email']

        hashed_password= bcrypt.hashpw(password, bcrypt.gensalt())
        conn= get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?,?)", 
                           (username, hashed_password, email))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exits, Please choose a different username"
        conn.close()
        return redirect(url_for('registered'))
    return render_template('signup.html')
#after Registration, user will be landed on a page to show "You have sucessfully Reistered"
@app.route('/registered')
def registered():
    return render_template('registered.html')

#creatimg A secure Login with 2 Factor authentication
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password'].encode('utf-8')

        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user=cursor.fetchone()

        if user:
            stored_password=user['password']
            if bcrypt.checkpw(password, stored_password):
                code = generate_code()
                email=user['email']

                cursor.execute("UPDATE users SET CODE=? WHERE username=?", (code,username))
                conn.commit()
                conn.close()

                session['username']=username
                session['code']=code

                send_verification_mail(email,code)
                return redirect(url_for('enter_code'))\
            
        return render_template('error.html')
    return render_template('login.html')

#Creating a function for randoring a page for entering OTP
@app.route('/enter_code')
def enter_code():
    return render_template('enter_code.html')

#function for verifying Code
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method=='POST':
        code_entered=request.form['code']
        username=session['username']
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT code from users where username=?", (username,))
        row=cursor.fetchone()
        cursor.close()

        if row and row['code']==code_entered:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute("UPDATE users SET code=NULL where username=?", (username,))
            conn.commit()
            conn.close()



#Creating a funtion for sending OTP on mail
@app.route("/")
def send_verification_mail():
    pass


#defining a function to generate OTP 
def generate_code():
    return str(random.randint(100000,999999))


#defining Database connection
def get_db_connection():
    conn=sqlite3.connect('users.db')
    conn.row_factory=sqlite3.Row
    return conn 

@app.route('/')
def show_login():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)
