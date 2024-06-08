from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from db import connect_db, insert_user, login_user
# from flask_bcrypt import Bcrypt
import bcrypt
import sys
app = Flask(__name__)

# Configure the secret key (choose a strong key for production)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # return print("getting here")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Server-side validation (optional, improve based on your needs)
        errors = {}
        if not name:
            errors['name_error'] = "Name is required."
        if not email or '@' not in email:
            errors['email_error'] = "Invalid email address."
        if not password:
            errors['password_error'] = "password not provided"

        if errors:
            return render_template('register.html', errors=errors)  # Pass errors to template

        # encrypt data
        # pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        # pw_hash = bcrypt.generate_password_hash(‘hunter2’).decode(‘utf-8’)
        # Insert user data if validation passes

        hashed = bcrypt.hashpw(password.encode('utf-8'), bytes(bcrypt.gensalt()))
        conn = connect_db()
        insert_user(conn, name, email, hashed)
        conn.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('show_users'))

    return render_template('register.html')


@app.route('/users')
def show_users():
    # Connect to database and fetch all users
    if session.get("email"):

        conn = connect_db()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()

        return render_template('users.html', users=users)

    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')  # Encode password for hashing
        
        # Connect to database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        login_data = cursor.fetchone()
        conn.close()

        if login_data:  # Check if user exists
            
            if bcrypt.checkpw(password, login_data[2]):
                session["email"] = request.form['email']
                # flash('Login successful!', 'success')
                return redirect(url_for('show_users'))  # Redirect after successful login
            else:
                flash('Invalid password.', 'error')
        else:
            flash('Invalid username or password.', 'error')

        return render_template('login.html')

@app.route("/view_profile/<id>")
def view_profile(id):
    
    return render_template('view_profile.html')

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0',port=5555)6
