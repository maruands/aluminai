from flask import Flask, render_template, request, redirect, url_for, flash
from db import connect_db, insert_user
from flask_bcrypt import Bcrypt
# import bcrypt

app = Flask(__name__)

# Configure the secret key (choose a strong key for production)
app.config['SECRET_KEY'] = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Server-side validation (optional, improve based on your needs)
        errors = {}
        if not name:
            errors['name_error'] = "Name is required."
        if not email or '@' not in email:
            errors['email_error'] = "Invalid email address."

        if errors:
            return render_template('register.html', errors=errors)  # Pass errors to template

        # Insert user data if validation passes
        conn = connect_db()
        insert_user(conn, name, email)
        conn.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('show_users'))

    return render_template('register.html')


@app.route('/users')
def show_users():
    # Connect to database and fetch all users
    conn = connect_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return render_template('users.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # Encode password for hashing

        # Connect to database
        conn = connect_db()
        cursor = conn.cursor()

        # Fetch user data by username
        cursor.execute("SELECT * FROM logins WHERE username = ?", (username,))
        login_data = cursor.fetchone()
        conn.close()

        if login_data:  # Check if user exists
            # Hash password from form input (for comparison)
            hashed_password = bcrypt.hashpw(password, login_data[1])  # login_data[1] assumes password col index

            # Compare hashed passwords
            if bcrypt.checkpw(password, hashed_password):
                flash('Login successful!', 'success')
                return redirect(url_for('show_users'))  # Redirect after successful login
            else:
                flash('Invalid password.', 'error')
        else:
            flash('Invalid username or password.', 'error')

        return render_template('login.html')
    return render_template('login.html')

    # pw_hash = bcrypt.generate_password_hash('hunter2')
    # bcrypt.check_password_hash(pw_hash, 'hunter2') # returns True

if __name__ == '__main__':
    app.run(debug=True)
