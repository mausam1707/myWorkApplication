from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import sqlite3


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
