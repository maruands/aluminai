import sqlite3
import bcrypt # Import bcrypt for password hashing

def connect_db():
    conn = sqlite3.connect('users.db')  # Replace 'users.db' with your desired filename
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS logins (username TEXT PRIMARY KEY, password TEXT)')
    return conn

def insert_user(conn, name, email):
    conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()

def insert_login(conn, username, hashed_password):
    conn.execute('INSERT INTO logins (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

