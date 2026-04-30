# utils.py - Helper utilities
# Various helper functions for the student management system
import datetime
import os


# Format a student name for display
def format_name(name):
    parts = name.split(" ")
    if len(parts) == 2:
        return parts[1] + ", " + parts[0]
    elif len(parts) == 3:
        return parts[2] + ", " + parts[0] + " " + parts[1]
    else:
        return name


# Format a student name for reports (same logic, slightly different)
def format_name_for_report(name):
    parts = name.split(" ")
    if len(parts) == 2:
        return parts[1].upper() + ", " + parts[0]
    elif len(parts) == 3:
        return parts[2].upper() + ", " + parts[0] + " " + parts[1]
    else:
        return name


# Format a student name for emails
def format_name_for_email(name):
    parts = name.split(" ")
    if len(parts) >= 2:
        return parts[0] + " " + parts[-1][0] + "."
    return name


def validate_email(email):
    # Check if email is valid
    if email is None:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    # Make sure there's something before and after @
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if len(parts[0]) == 0:
        return False
    if len(parts[1]) == 0:
        return False
    return True


def validate_phone(phone):
    # Check if phone number is valid
    if phone is None:
        return False
    digits = ""
    for ch in phone:
        if ch.isdigit():
            digits += ch
    if len(digits) < 10 or len(digits) > 15:
        return False
    return True


# Calculate letter grade from numeric average
def get_letter_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"


# This function was used for the old reporting system
# Keeping it in case we need it again
def generate_old_report(students, semester, year):
    report = "SEMESTER REPORT\n"
    report += "=" * 40 + "\n"
    report += f"Semester: {semester} {year}\n"
    report += f"Total Students: {len(students)}\n"
    for s in students:
        report += f"  {s.name}: {s.final_grade}\n"
    return report


# Another old function
def export_to_xml(students):
    xml = '<?xml version="1.0"?>\n<students>\n'
    for s in students:
        xml += f'  <student id="{s.student_id}">\n'
        xml += f'    <name>{s.name}</name>\n'
        xml += f'  </student>\n'
    xml += '</students>'
    return xml


def get_current_semester():
    month = datetime.datetime.now().month
    if month >= 1 and month <= 5:
        return "Spring"
    elif month >= 6 and month <= 8:
        return "Summer"
    else:
        return "Fall"


def log_action(action, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {action}: {details}")
