"""Helper utilities for the student management system."""
import datetime


TOTAL_CLASSES = 40
GPA_DIVISOR = 25
SCHOLARSHIP_MIN_AVERAGE = 85
SCHOLARSHIP_MIN_ATTENDANCE = 35
REPORT_WIDTH = 60


def format_name(name):
    """Format a name as Last, First for display."""
    return _format_name(name, uppercase_last_name=False)


def format_name_for_report(name):
    """Format a name as LAST, First for reports."""
    return _format_name(name, uppercase_last_name=True)


def format_name_for_email(name):
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[-1][0]}."
    return name


def _format_name(name, uppercase_last_name):
    parts = name.split()
    if len(parts) < 2:
        return name

    first_names = " ".join(parts[:-1])
    last_name = parts[-1].upper() if uppercase_last_name else parts[-1]
    return f"{last_name}, {first_names}"


def validate_email(email):
    if not email or email.count("@") != 1:
        return False

    local_part, domain = email.split("@")
    return bool(local_part and domain and "." in domain)


def validate_phone(phone):
    if phone is None:
        return False

    digits = "".join(character for character in phone if character.isdigit())
    return 10 <= len(digits) <= 15


def get_letter_grade(avg):
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def calculate_average(values):
    return sum(values) / len(values) if values else 0


def calculate_gpa(average):
    return average / GPA_DIVISOR


def calculate_attendance_rate(attendance_count):
    return attendance_count / TOTAL_CLASSES * 100


def generate_old_report(students, semester, year):
    lines = [
        "SEMESTER REPORT",
        "=" * 40,
        f"Semester: {semester} {year}",
        f"Total Students: {len(students)}",
        ]
    lines.extend(f"  {student.name}: {student.final_grade}" for student in students)
    return "\n".join(lines) + "\n"


def export_to_xml(students):
    lines = ['<?xml version="1.0"?>', "<students>"]
    for student in students:
        lines.append(f'  <student id="{student.student_id}">')
        lines.append(f"    <name>{student.name}</name>")
        lines.append("  </student>")
    lines.append("</students>")
    return "\n".join(lines)


def get_current_semester():
    month = datetime.datetime.now().month
    if 1 <= month <= 5:
        return "Spring"
    if 6 <= month <= 8:
        return "Summer"
    return "Fall"


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_action(action, details):
    print(f"[{current_timestamp()}] {action}: {details}")