
import smtplib
from email.mime.text import MIMEText
from context import UserSessionContext
from datetime import datetime
from utils.error_handler import handle_operation

def send_progress_email(context: UserSessionContext, recipient_email: str, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
    """
    Send an email with the user's progress summary.
    
    Args:
        context (UserSessionContext): The user's session context.
        recipient_email (str): The recipient's email address.
        smtp_server (str): SMTP server (e.g., 'smtp.gmail.com').
        smtp_port (int): SMTP port (e.g., 587 for TLS).
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password or app-specific password.
    
    Returns:
        dict: Success or error message.
    """
    def _send_email():
        # Prepare email content
        subject = f"Health & Wellness Progress Update for {context.name}"
        body = f"Health & Wellness Progress Update\n"
        body += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        body += "Goals:\n"
        if context.goal:
            body += (f"Action: {context.goal.get('action', 'N/A')}, "
                     f"Amount: {context.goal.get('amount', 'N/A')} {context.goal.get('unit', 'N/A')}, "
                     f"Duration: {context.goal.get('duration', 'N/A')} {context.goal.get('duration_unit', 'N/A')}\n")
        else:
            body += "No goals set yet.\n"
        body += "\nDietary Preferences:\n"
        body += context.diet_preferences or "None specified\n"
        body += "\nMeal Plan:\n"
        if context.meal_plan:
            for meal in context.meal_plan:
                body += f"- {meal}\n"
        else:
            body += "No meal plan set yet.\n"
        body += "\nWorkout Plan:\n"
        if context.workout_plan:
            for day in context.workout_plan.get('days', []):
                body += f"- {day['day']}: {', '.join(day['exercises'])}\n"
        else:
            body += "No workout plan set yet.\n"
        body += "\nHandoff Logs:\n"
        body += "\n".join(context.handoff_logs) if context.handoff_logs else "No handoff logs available.\n"
        body += "\nProgress Logs:\n"
        for log in context.progress_logs:
            body += f"- {log['timestamp']}: {log['event']}\n" if context.progress_logs else "No progress logs available.\n"

        # Create email message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return {"message": f"Progress email sent to {recipient_email}"}

    return handle_operation(_send_email, context=context)
