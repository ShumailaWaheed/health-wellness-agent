import sqlite3
import json
from typing import Optional
from context import UserSessionContext

class DatabaseManager:
    def __init__(self, db_path: str = "health_wellness.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        # Create the 'users' table if it doesn't exist already
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid INTEGER PRIMARY KEY,
                    name TEXT,
                    goal TEXT,
                    diet_preferences TEXT,
                    workout_plan TEXT,
                    meal_plan TEXT,
                    injury_notes TEXT,
                    handoff_logs TEXT,
                    progress_logs TEXT
                )
            """)
            conn.commit()

    def save_context(self, context: UserSessionContext):
        # Save or update user session context in the database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO users (
                    uid, name, goal, diet_preferences, workout_plan,
                    meal_plan, injury_notes, handoff_logs, progress_logs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                context.uid,
                context.name,
                json.dumps(context.goal),
                context.diet_preferences,
                json.dumps(context.workout_plan),
                json.dumps(context.meal_plan),
                context.injury_notes,
                json.dumps(context.handoff_logs),
                json.dumps(context.progress_logs)
            ))

            conn.commit()

    def load_context(self, uid: int) -> Optional[UserSessionContext]:
        # Load a user's session context from the database using their UID
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
            row = cursor.fetchone()

            if row:
                return UserSessionContext(
                    uid=row[0],
                    name=row[1],
                    goal=json.loads(row[2]) if row[2] else None,
                    diet_preferences=row[3],
                    workout_plan=json.loads(row[4]) if row[4] else None,
                    meal_plan=json.loads(row[5]) if row[5] else None,
                    injury_notes=row[6],
                    handoff_logs=json.loads(row[7]) if row[7] else [],
                    progress_logs=json.loads(row[8]) if row[8] else []
                )

        return None
