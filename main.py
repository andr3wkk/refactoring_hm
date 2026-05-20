#!/usr/bin/env python3
"""
Student Grade Management System
================================
A system for processing student grades, attendance, and generating reports.

Run: python3 main.py
"""
from models import Student
from student_manager import StudentManager
from utils import get_current_semester, log_action


def create_sample_students():
    """Create sample student data for demonstration."""
    students = [
        Student("Alice Johnson", 1001, "alice@university.edu",
                [92, 88, 95, 91, 87], 38,
                3, "Computer Science", "555-0101", "123 Campus Dr",
                "Bob Johnson (555-0102)", "2022-09-01", False),
        Student("Bob Smith", 1002, "bob@university.edu",
                [75, 82, 68, 71, 79], 32,
                2, "Mathematics", "555-0201", "456 College Ave",
                "Mary Smith (555-0202)", "2023-09-01", False),
        Student("Carol Williams", 1003, "carol@university.edu",
                [95, 98, 92, 97, 94], 40,
                4, "Computer Science", "555-0301", "789 University Blvd",
                "Dan Williams (555-0302)", "2021-09-01", True),
        Student("David Brown", 1004, "david@university.edu",
                [55, 62, 48, 59, 51], 18,
                1, "Business", "555-0401", "321 Dorm Rd",
                "Lisa Brown (555-0402)", "2024-09-01", False),
        Student("Eva Martinez", 1005, "eva@university.edu",
                [88, 85, 90, 82, 86], 36,
                3, "Engineering", "555-0501", "654 Tech Park",
                "Carlos Martinez (555-0502)", "2022-09-01", True),
        Student("Frank Lee", 1006, "frank@university.edu",
                [72, 68, 74, 65, 70], 25,
                2, "Physics", "555-0601", "987 Science Dr",
                "Grace Lee (555-0602)", "2023-09-01", False),
        Student("Grace Kim", 1007, "grace@university.edu",
                [98, 96, 99, 95, 97], 39,
                4, "Computer Science", "555-0701", "147 Grad Hall",
                "James Kim (555-0702)", "2021-09-01", False),
        Student("Henry Davis", 1008, "henry@university.edu",
                [61, 58, 65, 55, 63], 28,
                1, "Art", "555-0801", "258 Creative Ave",
                "Sara Davis (555-0802)", "2024-09-01", False),
    ]
    return students


def main():
    print("=" * 60)
    print("  STUDENT GRADE MANAGEMENT SYSTEM")
    print(f"  Semester: {get_current_semester()} 2026")
    print("=" * 60)
    print()

    manager = StudentManager()

    students = create_sample_students()
    for student in students:
        manager.add_student(student)

    log_action("SYSTEM", f"Loaded {len(students)} students")

    print(">>> Processing Grades...")
    graded = manager.process_grades(
        send_notifications=True,
        notification_prefix="Dear"
    )
    print(f"    Processed {len(graded)} students for grading.\n")

    print(">>> Processing Attendance...")
    attended = manager.process_attendance(
        min_attendance_pct=75,
        include_warnings=True,
        send_notifications=True,
        notification_prefix="Important:"
    )
    print(f"    Processed {len(attended)} students for attendance.\n")

    print(">>> Updating Student Statuses...")
    manager.update_statuses()
    print("    Statuses updated.\n")

    print(">>> Generating Grade Report...")
    grade_report = manager.generate_report(
        students=manager.students,
        report_type="grades",
        include_header=True,
        include_summary=True,
        sort_by="grade",
        output_file=None
    )
    print(grade_report)
    print()

    print(">>> Generating Attendance Report...")
    attendance_report = manager.generate_report(
        students=manager.students,
        report_type="attendance",
        include_header=True,
        include_summary=True,
        sort_by="attendance",
        output_file=None
    )
    print(attendance_report)
    print()

    print(">>> Statistics Summary...")
    stats = manager.get_statistics(manager.students)
    print(f"    Total Students:        {stats['total']}")
    print(f"    Average GPA:           {stats['avg_gpa']}")
    print(f"    Highest GPA:           {stats['highest_gpa']}")
    print(f"    Lowest GPA:            {stats['lowest_gpa']}")
    print(f"    Pass Rate:             {stats['pass_rate']}%")
    print(f"    Scholarship Eligible:  {stats['scholarship_eligible']}")
    print(f"    Attendance Warnings:   {stats['warnings']}")
    print(f"    Grade Distribution:    A={stats['grade_a']} B={stats['grade_b']} C={stats['grade_c']} D={stats['grade_d']} F={stats['grade_f']}")
    print()

    print(">>> Notifications Log...")
    for notification in manager.notification_log:
        print(f"    [{notification['sent_at']}] To: {notification['to']} | Type: {notification['type']}")
        print(f"      Message: {notification['message']}")
    print()

    print("=" * 60)
    print("  Processing Complete.")
    print(f"  Total operations: {manager.processed_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()