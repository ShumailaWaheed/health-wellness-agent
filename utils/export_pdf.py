import io
from datetime import datetime
from context import UserSessionContext

def generate_progress_report(context: UserSessionContext) -> dict:
    try:
        # Safely get context values or provide defaults
        name = context.name or "N/A"
        email = context.email or "N/A"
        goal = context.goal or "No goal set"
        diet = ", ".join(context.diet_preferences) if context.diet_preferences else "Not specified"
        health_conditions = ", ".join(context.health_conditions) if context.health_conditions else "None"

        report_lines = []
        report_lines.append("📋 Health & Wellness Progress Report")
        report_lines.append("====================================\n")
        report_lines.append(f"🧑 Name: {name}")
        report_lines.append(f"📧 Email: {email}")
        report_lines.append(f"🎯 Goal: {goal}")
        report_lines.append(f"🥗 Dietary Preferences: {diet}")
        report_lines.append(f"🩺 Health Conditions: {health_conditions}")
        report_lines.append(f"📅 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report_lines.append("📝 Progress Logs:")
        if context.progress_logs:
            for log in context.progress_logs:
                timestamp = log.get("timestamp", "Unknown time")
                event = log.get("event", "No event")
                report_lines.append(f"• {timestamp} - {event}")
        else:
            report_lines.append("• No progress logs available.")

        report_lines.append("\n🗣️ Handoff Consultations:")
        if context.handoff_logs:
            for log in context.handoff_logs:
                report_lines.append(f"• {log}")
        else:
            report_lines.append("• No consultations recorded.")

        # Combine all into a single string
        full_report = "\n".join(report_lines)

        # Create an in-memory file (for download)
        file_buffer = io.StringIO()
        file_buffer.write(full_report)
        file_buffer.seek(0)

        return {
            "message": "✅ Report generated successfully.",
            "file": file_buffer.getvalue()
        }

    except Exception as e:
        return {"error": f"❌ Failed to generate report: {str(e)}"}
