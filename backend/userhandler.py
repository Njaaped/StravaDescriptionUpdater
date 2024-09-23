import sqlite3
from gettokens import get_refresh_token
import os
from dotenv import load_dotenv

class UserHandler:

    USERNAME_MAX_LEN = 20
    PASSWORD_MAX_LEN = 20

    USERNAME_MIN_LEN = 5
    PASSWORD_MIN_LEN = 5

    LEGAL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:',.<>/?`~"

    load_dotenv()
    DATABASE_PATH = os.getenv('DATABASE_FILE')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    def check_login(self, data):
        """Check if user exists in the database and has a refresh token."""
        username = data['username']
        password = data['password']
        return (
            self.check_user_in_database(username, password),
            self.check_user_refresh_token(username)
        )
    
    def check_user_in_database(self, username, password):
        """Check if the username and password match a record in the database."""
        query = "SELECT * FROM users WHERE username=? AND password=?"
        return self.fetch_one(query, (username, password)) is not None
    
    def check_user_refresh_token(self, username):
        """Check if the user has a refresh token in the database."""
        query = "SELECT * FROM userRefreshToken WHERE username=?"
        return self.fetch_one(query, (username,)) is not None
    
    def add_user_with_code(self, data):
        """Add a user refresh token using a code."""
        return self.add_refresh_token_to_db(data['username'], data['code'])
    
    def add_user(self, data):
        """Add a new user to the database."""
        username = data['username']
        password = data['password']
        if not self.is_valid_username(username) or not self.is_valid_password(password):
            return False
        return self.add_user_to_database(username, password)
    
    def is_valid_username(self, username):
        """Validate the username based on length and legal characters."""
        return (self.USERNAME_MIN_LEN <= len(username) <= self.USERNAME_MAX_LEN and
                all(char in self.LEGAL_CHARS for char in username))
    
    def is_valid_password(self, password):
        """Validate the password based on length and legal characters."""
        return (self.PASSWORD_MIN_LEN <= len(password) <= self.PASSWORD_MAX_LEN and
                all(char in self.LEGAL_CHARS for char in password))
    
    def add_user_to_database(self, username, password):
        """Insert a new user into the database."""
        queries = [
            ("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)),
            ("INSERT INTO description (username, type, description) VALUES (?, ?, '')", (username, "Run")),
            ("INSERT INTO description (username, type, description) VALUES (?, ?, '')", (username, "Ride")),
        ]
        return self.execute_queries(queries)
    
    def add_refresh_token_to_db(self, username, code):
        """Insert a new refresh token into the database."""
        if self.check_user_refresh_token(username):
            print("User already exists, skipping insertion.")
            return True

        refresh_token, user_id = get_refresh_token(code, self.CLIENT_ID, self.CLIENT_SECRET)
        queries = [
            ("INSERT INTO userRefreshToken (username, refreshToken) VALUES (?, ?)", (username, refresh_token)),
            ("INSERT INTO usernameStravaId (username, id) VALUES (?, ?)", (username, user_id)),
        ]
        return self.execute_queries(queries)

    def fetch_one(self, query, params):
        """Fetch a single record from the database."""
        with sqlite3.connect(self.DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def execute_queries(self, queries):
        """Execute multiple queries within a transaction."""
        try:
            with sqlite3.connect(self.DATABASE_PATH) as conn:
                cursor = conn.cursor()
                for query, params in queries:
                    cursor.execute(query, params)
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return False
        
        




