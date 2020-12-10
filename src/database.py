import sqlite3

# Upon the file being opened, create a connection to the database.
db = sqlite3.connect(":memory:")

# Create a table for the users and scores if one doesn't already exist.
# - Username: String (30 chars max, cannot be nothing, unique regardless of case).
# - Password: String (cannot be nothing)
# - Score: Integer (default 0, cannot be nothing)

db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(30) PRIMARY KEY,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0 NOT NULL,

        UNIQUE (username COLLATE NOCASE)
    ) 
''')

# Methods to make interacting with the database quick and simple.

# Sort all users in the database from lowest score to highest, then return the top 5 entries.
def fetch_leaderboard():
    top_users = db.execute('SELECT * FROM users ORDER BY score ASC LIMIT 5').fetchall()
    
    # Parse the results into a dictionary.
    top_users_parsed = []
    
    for user in top_users:
        top_users_parsed.append({
          "username": user[0],
          "password": user[1],
          "score": user[2]
        })
        
    # Return the data.
    return top_users_parsed
            
# Fetch the account by username, ignore the username's case.
def fetch_user_by_username(username: str):
    # Use SQLite's pre-prepared statements to avoid SQL Injection (in basic sense, ? gets replaced with username).
    # Turning username to a lowercase to accomodate the 'ignore case' SQL lookup.
    result = db.execute('SELECT * FROM users WHERE LOWER(username) = ?', (username.lower(),)).fetchone()

    # If user doesn't exist, return nothing.
    if not result:
        return None

    # Return the user as an object to make retrieving data simple (since sqlite returns it unlabaled).
    return {
        "username": result[0],
        "password": result[1],
        "score": result[2]
    }

# Create a user with a username and password.
def create_user(username: str, password: str):
    # Create a database record for the table 'users' with the user's username and password.
    db.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, password))

    # Fetch the created user.
    user = db.execute('SELECT * FROM users WHERE LOWER(username) = ?', (username,)).fetchone()

    # Return the user.
    return {
        "username": user[0],
        "password": user[1],
        "score": user[2]
    }

# Closes the database connection, done at program end.
def close_connection():
    db.close()
