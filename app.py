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

@app.route("/")
def home():
    return render_template("index.html")

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
                return redirect(url_for('home'))  # Redirect after successful login
            else:
                flash('Invalid password.', 'error')
        else:
            flash('Invalid username or password.', 'error')

        return render_template('login.html')

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

        hashed = bcrypt.hashpw(password.encode('utf-8'), bytes(bcrypt.gensalt()))
        conn = connect_db()
        insert_user(conn, firstname.upper(), surname.upper(), email, hashed)
        conn.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('show_users'))

    return render_template('register.html')


@app.route('/alumni')
def show_users():
    # Connect to database and fetch all users
    if session.get("email"):

        conn = connect_db()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        # return f'{users}'
        return render_template('alumni.html', users=users)

    return render_template('login.html')




@app.route("/view_profile/<id>")
def view_profile(id):
    if session.get("email"):
        return render_template('view_profile.html')
    
    return render_template('login.html')

@app.route("/dashbord")
def dashboard():
    if session.get("email"):
        return render_template('index.html')
    return render_template('login.html')

@app.route("/news")
def news():
    if session.get("email"):
        return render_template('news.html')
    return render_template('login.html')
    
@app.route("/prof/<email>")
def prof(email):
    # Connect to database
    if session.get("email"):
        conn = connect_db()
        cursor = conn.cursor()
        user = conn.execute("SELECT users.firstname, users.surname, users.email, profiles.education, profiles.location, profiles.bio, profiles.year FROM users INNER JOIN profiles ON users.id=profiles.user_id WHERE users.email = ?", (email,)).fetchone()
        if not user:
            user=conn.execute("SELECT users.firstname, users.surname, users.email FROM users WHERE users.email = ?", (email,)).fetchone()
        conn.close()
        return render_template('prof.html', user=user)
    return render_template('login.html')

@app.route("/edit_profile<email>")
def edit_profile(email):
    print(email)
    return render_template('edit_profile.html', id=email)

@app.route("/profile", methods=['POST'])
def profile():
    if request.method == 'POST':
        user_id = request.form['id']
        education = request.form['education']
        location = request.form['location']
        year = request.form['year']
        bio = request.form['bio']
        house = request.form['house']
        print(user_id,education,location,bio,year,house)
        conn = connect_db()
        inser_profile(conn,user_id,education,location,bio,year,house)
        conn.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('edit_profile', id=user_id))

@app.route("/myprofile/<email>")
def myprofile(email):
    print(email)
    conn = connect_db()
    cursor = conn.cursor()
    user = conn.execute("SELECT users.firstname, users.surname, users.email, profiles.education, profiles.location, profiles.bio, profiles.year FROM users INNER JOIN profiles ON users.id=profiles.user_id WHERE users.email = ?", (email,)).fetchone()
    conn.close()
    print(user)
    return render_template("prof.html", user=user)

@app.route("/search_user", methods=[ 'POST'])
def search_user():
    if request.method == 'POST':
        name = request.form['name']
        
        # Connect to database
        conn = connect_db()
        cursor = conn.cursor()
        users = conn.execute("SELECT * FROM users WHERE firstname = ?", (name.upper(),)).fetchall()
        if not users:
            users = conn.execute("SELECT * FROM users WHERE surname = ?", (name.upper(),)).fetchall()
        conn.close()
        # return f'{users}'
        return render_template('alumni.html', users=users)    
    
@app.route("/logout")
def logout():
    # session["email"] = None
    print(session["email"])
    session.clear()
    return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0',port=5555)6
