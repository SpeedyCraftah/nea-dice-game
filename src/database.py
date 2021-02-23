import sqlite3
import atexit
import os

# Path to the SQLite file.
# Pass the path into path#normcase to replace '/' with '\' if the operating system is Windows.
dbPath = os.path.normcase("./database/db.sqlite")

# Create a connection to the database passing the path of the SQLite file.
db = sqlite3.connect(dbPath, timeout=5)

# Register an event callback that automatically gets called on program SIGINT/SIGTERM (exit).
atexit.register(lambda: db.close())

# Create a table for the users and scores if one doesn't already exist.
# - Username: String (30 chars max, cannot be nothing, unique regardless of case)
# - Password: String (cannot be nothing)
# - Score: Integer (default 0, cannot be nothing)
db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(30),
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0 NOT NULL,

        UNIQUE (username COLLATE NOCASE)
    ) 
''')

# Save the changes to the database file.
db.commit()

# Methods to make interacting with the database quick and simple.

# Sort all users in the database from lowest score to highest, then return the top 5 entries.
def fetch_leaderboard():
    top_users = db.execute('SELECT * FROM users ORDER BY score DESC LIMIT 5').fetchall()
    
    # Parse the results into a dictionary.
    top_users_parsed = []
    
    # Use the 'enumerate' function to also get an index while iterating (this will be the position).
    for index, user in enumerate(top_users):
        top_users_parsed.append({
            "position": index + 1,
            "id": user[0],
            "username": user[1],
            "password": user[2],
            "score": user[3]
        })
        
    # Return the data.
    return top_users_parsed
            
# Fetch the account by username.
def fetch_user_by_username(username: str):
    # Use SQLite's pre-prepared statements to avoid SQL Injection (in basic sense, ? gets replaced with username)
    # causing the SQLite engine to treat the passed data ONLY as data and not SQL statements.
    # Turning username to a lowercase to accomodate the 'ignore case' SQL lookup
    result = db.execute('SELECT * FROM users WHERE LOWER(username) = ?', (username.lower(),)).fetchone()

    # If user doesn't exist, return nothing.
    if not result:
        return None

    # Return the user as an object to make retrieving data simple (since sqlite returns it unlabaled).
    return {
        "id": result[0],
        "username": result[1],
        "password": result[2],
        "score": result[3]
    }

# Create a user with a username and password.
def create_user(username: str, password: str):
    # Create a database record for the table 'users' with the user's username and password.
    db.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, password))

    # Fetch the created user with an already defined lookup method.
    user = fetch_user_by_username(username)

    # Save the changes to the database file.
    db.commit()

    # Return the user.
    return user

# Update the players score.
def update_user_score(username: str, new_score: int):
    db.execute('''
        UPDATE users SET score = ? WHERE username = ?
    ''', (new_score, username))

    # Save the changes to the database file.
    db.commit()

# Closes the database connection, done at program end.
def close_connection():
    db.close()
