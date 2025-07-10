# utils/user_auth.py

import sqlite3
import uuid
from context import UserSessionContext
from utils.error_handler import handle_operation

class UserAuth:
    def __init__(self, db_path: str = "health_wellness.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    uid INTEGER
                )
            """)
            # Make sure all required columns are present
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]

            if 'email' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            if 'username' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
            if 'password' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
            if 'uid' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN uid INTEGER")

            conn.commit()

    def authenticate_user(self, email, password):
        # Inner function to handle the login process
        def _auth():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username, uid FROM users WHERE email = ? AND password = ?",
                    (email, password)
                )
                result = cursor.fetchone()

                if result:
                    return {
                        "uid": result[1],
                        "message": "Login successful",
                        "username": result[0]
                    }

                return {"error": "Invalid email or password"}

        # Use error handler to execute login
        return handle_operation(_auth)

    def register_user(self, username, email, password):
        # Inner function to handle registration logic
        def _register():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if email is already registered
                cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                    return {"error": "Email already registered"}

                # Generate a unique user ID
                uid = uuid.uuid4().int & (1 << 31) - 1

                # Insert new user into the database
                cursor.execute(
                    "INSERT INTO users (email, username, password, uid) VALUES (?, ?, ?, ?)",
                    (email, username, password, uid)
                )

                conn.commit()
                return {
                    "message": "User registered",
                    "uid": uid
                }

        # Use error handler to execute registration
        return handle_operation(_register)
