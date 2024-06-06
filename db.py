import sqlite3
import bcrypt # Import bcrypt for password hashing

def connect_db():
    # conn = sqlite3.connect('users.db')  # Replace 'users.db' with your desired filename
    conn = sqlite3.connect('members.db')  # Replace 'users.db' with your desired filename
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS logins (username TEXT PRIMARY KEY, password TEXT)')
    return conn
def login_user(conn, email):
    conn.execute('SELECT * FROM users where email=?', (email,))

def insert_user(conn, name, email, password):
    conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    conn.commit()

def insert_login(conn, username, hashed_password):
    conn.execute('INSERT INTO logins (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

