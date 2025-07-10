def generate_progress_report(context):
    # Pre-compute values to avoid backslashes in f-string expressions
    timestamp = getattr(context, 'timestamp', 'Unknown')
    name = getattr(context, 'name', 'User')
    email = getattr(context, 'email', 'No email')
    goal = getattr(context, 'goal', 'Not set')
    preferences = ', '.join(getattr(context, 'diet_preferences', []) or ['None'])
    conditions = ', '.join(getattr(context, 'health_conditions', []) or ['None'])
    
    # Format handoff_logs and progress_logs with LaTeX
    handoff_logs = ''
    for log in getattr(context, 'handoff_logs', []):
        parts = log.split('|')
        if len(parts) >= 3:
            handoff_logs += f'\\item Query: {parts[0].strip()}\\\\ Response: {parts[1].strip()}\\\\ Time: {parts[2].strip()}\\n'
    handoff_logs = handoff_logs or 'No consultation history.'
    
    progress_logs = ''
    for log in getattr(context, 'progress_logs', []):
        progress_logs += f'\\item Event: {log["event"]}\\\\ Time: {log["timestamp"]}\\n'
    progress_logs = progress_logs or 'No progress logs.'
    
    # Construct LaTeX content using concatenation
    latex_content = (
        "\\documentclass[a4paper,12pt]{article}\n"
        "\\usepackage{geometry}\n"
        "\\usepackage{parskip}\n"
        "\\usepackage{noto}\n"
        "\\geometry{margin=1in}\n\n"
        "\\begin{document}\n"
        "\\section*{HealthSync Wellness Progress Report}\n"
        "\\textbf{Generated}: " + timestamp + "\\\\\n"
        "\\textbf{User}: " + name + " (" + email + ")\\\\\n"
        "\\textbf{Goal}: " + goal + "\\\\\n"
        "\\textbf{Dietary Preferences}: " + preferences + "\\\\\n"
        "\\textbf{Health Conditions}: " + conditions + "\\\\\n\n"
        "\\subsection*{Consultation History}\n"
        + handoff_logs + "\n\n"
        "\\subsection*{Progress Logs}\n"
        + progress_logs + "\n"
        "\\end{document}"
    )
    return {"message": "Report generated", "content": latex_content}