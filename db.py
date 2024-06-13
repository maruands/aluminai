import sqlite3
import bcrypt # Import bcrypt for password hashing

def connect_db():
    conn = sqlite3.connect('users.db')  # Replace 'users.db' with your desired filename
    # conn = sqlite3.connect('members.db')  # Replace 'users.db' with your desired filename
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, surname TEXT, email TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS profiles (user_id INTEGER PRIMARY KEY, education TEXT, location  TEXT, bio TEXT, year INTEGER, house TEXT)')
    return conn

def login_user(conn, email):
    conn.execute('SELECT * FROM users where email=?', (email,))

def insert_user(conn, firstname, surname, email, password):
    conn.execute('INSERT INTO users (firstname, surname, email, password) VALUES (?, ?, ?, ?)', (firstname, surname, email, password))
    conn.commit()

def inser_profile(conn,user_id,education,location,bio,year,house):
    conn.execute('INSERT INTO profiles (user_id, education, location, bio, year, house) VALUES (?, ?, ?, ?, ?, ?)', (user_id,education,location,bio,year,house))
    conn.commit()

def insert_login(conn, username, hashed_password):
    conn.execute('INSERT INTO logins (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

