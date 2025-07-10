
import sqlite3
import pandas as pd
from context import UserSessionContext
from utils.error_handler import handle_operation
from datetime import datetime

class ActivityAnalytics:
    def __init__(self, db_path: str = "health_wellness.db"):
        self.db_path = db_path

    def analyze_activities(self, context: UserSessionContext) -> dict:
        """Analyze user activities to provide goal progress insights."""
        def _analyze():
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(
                    "SELECT activity_type, activity_details, timestamp FROM activities WHERE uid = ?",
                    conn,
                    params=(context.uid,),
                    parse_dates=['timestamp']
                )
            
            if df.empty:
                return {"message": "No activities found for analysis"}
            
            total_activities = len(df)
            goal_count = len(df[df['activity_type'] == 'Goal Submission'])
            feedback_count = len(df[df['activity_type'] == 'Feedback Submission'])
            profile_updates = len(df[df['activity_type'] == 'Profile Update'])
            
            df['date'] = df['timestamp'].dt.date
            activity_trend = df.groupby('date').size().to_dict()
            
            result = {
                "total_activities": total_activities,
                "goal_count": goal_count,
                "feedback_count": feedback_count,
                "profile_updates": profile_updates,
                "activity_trend": {str(date): count for date, count in activity_trend.items()},
                "message": "Analytics generated successfully"
            }
            
            context.progress_logs.append({
                "event": "Generated activity analytics",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return result
        
        return handle_operation(_analyze, context=context)
