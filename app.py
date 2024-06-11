from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from db import connect_db, insert_user, login_user, inser_profile
# from flask_bcrypt import Bcrypt
import bcrypt
import sys
app = Flask(__name__)

# Configure the secret key (choose a strong key for production)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # return print("getting here")
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        # Server-side validation (optional, improve based on your needs)
        errors = {}
        if not firstname:
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
        insert_user(conn, firstname, surname, email, hashed)
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
        # return f'{users}'
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
        print(login_data)
        conn.close()

        if login_data:  # Check if user exists
            
            if bcrypt.checkpw(password, login_data[4]):
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


@app.route("/")
def dashboard():
    return render_template('index.html')

@app.route("/news")
def news():
    return render_template('news.html')

@app.route("/prof<id>")
def prof(id):
    # Connect to database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()

    cursor.execute("select * FROM profiles where user_id = ?", (id,))
    profile = cursor.fetchone()
    
    conn.close()
    return render_template('prof.html', user=user, profile=profile)

@app.route("/edit_profile<id>")
def edit_profile(id):
    print(id)
    return render_template('edit_profile.html', id=id)

@app.route("/profile", methods=['POST'])
def profile():
    if request.method == 'POST':
        user_id = request.form['id']
        education = request.form['education']
        location = request.form['location']
        year = request.form['year']
        bio = request.form['bio']
        house = request.form['house']

        conn = connect_db()
        inser_profile(conn,user_id,education,location,year,bio,house)
        conn.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('edit_profile', id=user_id))

@app.route("/search_user", methods=[ 'POST'])
def search_user():
    if request.method == 'POST':
        name = request.form['name']
        
        # Connect to database
        conn = connect_db()
        cursor = conn.cursor()
        users = conn.execute("SELECT * FROM users WHERE firstname = ?", (name,)).fetchall()
        conn.close()
        # return f'{users}'
        return render_template('users.html', users=users)    
    
@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0',port=5555)6
