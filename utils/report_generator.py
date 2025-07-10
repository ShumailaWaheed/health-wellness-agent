from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from context import UserSessionContext
from datetime import datetime

def generate_progress_report(context: UserSessionContext, output_path: str = "user_progress_report.pdf"):
    """
    Generate a PDF report of the user's health and wellness progress.
    
    Args:
        context (UserSessionContext): The user's session context containing goals, plans, and logs.
        output_path (str): Path to save the PDF report.
    """
    # Initialize PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title
    story.append(Paragraph(f"Health & Wellness Progress Report for {context.name}", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add goal section
    story.append(Paragraph("Goals", styles['Heading2']))
    if context.goal:
        goal_text = (f"Action: {context.goal.get('action', 'N/A')}, "
                     f"Amount: {context.goal.get('amount', 'N/A')} {context.goal.get('unit', 'N/A')}, "
                     f"Duration: {context.goal.get('duration', 'N/A')} {context.goal.get('duration_unit', 'N/A')}")
        story.append(Paragraph(goal_text, styles['Normal']))
    else:
        story.append(Paragraph("No goals set yet.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add dietary preferences
    story.append(Paragraph("Dietary Preferences", styles['Heading2']))
    story.append(Paragraph(context.diet_preferences or "None specified", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add meal plan
    story.append(Paragraph("Meal Plan", styles['Heading2']))
    if context.meal_plan:
        meal_data = [[f"Day {i+1}", meal] for i, meal in enumerate(context.meal_plan)]
        meal_table = Table(meal_data, colWidths=[100, 400])
        story.append(meal_table)
    else:
        story.append(Paragraph("No meal plan set yet.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add workout plan
    story.append(Paragraph("Workout Plan", styles['Heading2']))
    if context.workout_plan:
        workout_data = [[day['day'], ", ".join(day['exercises'])] for day in context.workout_plan.get('days', [])]
        workout_table = Table(workout_data, colWidths=[100, 400])
        story.append(workout_table)
    else:
        story.append(Paragraph("No workout plan set yet.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add injury notes
    story.append(Paragraph("Injury Notes", styles['Heading2']))
    story.append(Paragraph(context.injury_notes or "None specified", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add progress logs
    story.append(Paragraph("Progress Logs", styles['Heading2']))
    if context.progress_logs:
        log_data = [[log['timestamp'], log['event']] for log in context.progress_logs]
        log_table = Table(log_data, colWidths=[100, 400])
        story.append(log_table)
    else:
        story.append(Paragraph("No progress logs available.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add handoff logs
    story.append(Paragraph("Handoff Logs", styles['Heading2']))
    if context.handoff_logs:
        for log in context.handoff_logs:
            story.append(Paragraph(log, styles['Normal']))
    else:
        story.append(Paragraph("No handoff logs available.", styles['Normal']))

    # Build and save the PDF
    doc.build(story)
    return {"message": f"PDF report generated at {output_path}"}
