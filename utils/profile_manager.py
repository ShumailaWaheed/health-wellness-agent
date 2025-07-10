import sqlite3
from context import UserSessionContext
from utils.error_handler import handle_operation
from datetime import datetime

class ProfileManager:
    def __init__(self, db_path: str = "health_wellness.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the user_profiles table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    uid INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    preferences TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()

    def update_profile(self, context: UserSessionContext, name: str = None, email: str = None, preferences: str = None) -> dict:
        """Update user profile in the database and context."""
        def _update():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_profiles (uid, name, email, preferences, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (context.uid, name or context.name, email, preferences or context.diet_preferences, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
            
            if name:
                context.name = name
            if preferences:
                context.diet_preferences = preferences
            context.progress_logs.append({
                "event": f"Profile updated: name={name or context.name}, email={email}, preferences={preferences or context.diet_preferences}",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return {"message": "Profile updated successfully"}
        
        return handle_operation(_update, context=context)