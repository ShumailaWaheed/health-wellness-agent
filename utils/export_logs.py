
from context import UserSessionContext
from datetime import datetime

def export_logs(context: UserSessionContext, output_path: str = "user_logs.txt"):
    """
    Export handoff and progress logs to a text file.
    
    Args:
        context (UserSessionContext): The user's session context containing logs.
        output_path (str): Path to save the log file.
    """
    with open(output_path, 'w') as f:
        f.write(f"Health & Wellness Logs for {context.name} (UID: {context.uid})\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("Handoff Logs:\n")
        if context.handoff_logs:
            for log in context.handoff_logs:
                f.write(f"- {log}\n")
        else:
            f.write("No handoff logs available.\n")
        
        f.write("\nProgress Logs:\n")
        if context.progress_logs:
            for log in context.progress_logs:
                f.write(f"- {log['timestamp']}: {log['event']}\n")
        else:
            f.write("No progress logs available.\n")
    
    return {"message": f"Logs exported to {output_path}"}
