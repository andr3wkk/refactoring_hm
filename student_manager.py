"""Business logic for student grade management."""
import json
import os

from utils import (
    REPORT_WIDTH,
    SCHOLARSHIP_MIN_ATTENDANCE,
    SCHOLARSHIP_MIN_AVERAGE,
    TOTAL_CLASSES,
    calculate_attendance_rate,
    calculate_average,
    calculate_gpa,
    current_timestamp,
    format_name_for_report,
    get_letter_grade,
    log_action,
    validate_email,
)


class StudentManager:
    """Manages student processing, reports, notifications, and statistics."""

    def __init__(self):
        self.students = []
        self.processed_count = 0
        self.error_log = []
        self.notification_log = []

    def add_student(self, student):
        self.students.append(student)

    def process_grades(self, send_notifications=False, notification_prefix="Dear"):
        results = []
        for student in self.students:
            average = calculate_average(student.grades)
            student.final_grade = get_letter_grade(average)
            student.gpa = calculate_gpa(average)
            student.scholarship_eligible = self._is_scholarship_eligible(student, average)

            if send_notifications:
                message = (
                    f"{notification_prefix} {student.name}, your grade is {student.final_grade} "
                    f"(GPA: {round(student.gpa, 2)})"
                )
                self._send_notification(student, message, "grade")

            results.append(student)
            self._count_processed()
        return results

    def process_attendance(
            self,
            min_attendance_pct=75,
            include_warnings=True,
            send_notifications=False,
            notification_prefix="Important:",
    ):
        results = []
        for student in self.students:
            rate = calculate_attendance_rate(student.attendance_count)

            if rate < min_attendance_pct:
                student.warning = True
                if include_warnings:
                    student.notes.append(f"Low attendance warning: {round(rate, 1)}%")
                if send_notifications:
                    message = f"{notification_prefix} {student.name}, attendance warning: {round(rate, 1)}%"
                    self._send_notification(student, message, "attendance")

            results.append(student)
            self._count_processed()
        return results

    def update_statuses(self):
        results = []
        for student in self.students:
            if student.final_grade == "F":
                student.status = "probation"
            elif student.warning:
                student.status = "warning"
            else:
                student.status = "good_standing"

            results.append(student)
            self._count_processed()
        return results

    def process_students(
            self,
            mode,
            output_dir=None,
            send_notifications=False,
            notification_prefix="",
            min_attendance_pct=75,
            include_warnings=True,
            export_format="json",
    ):
        """Backward-compatible wrapper for the original mode-based API."""
        if mode == "grade":
            return self.process_grades(send_notifications, notification_prefix)
        if mode == "attendance":
            return self.process_attendance(
                min_attendance_pct,
                include_warnings,
                send_notifications,
                notification_prefix,
            )
        if mode == "status":
            return self.update_statuses()
        return []

    def generate_report(
            self,
            students,
            report_type,
            include_header,
            include_summary,
            sort_by,
            output_file,
    ):
        report_builders = {
            "grades": self._build_grade_report,
            "attendance": self._build_attendance_report,
            "full": self._build_full_report,
        }
        builder = report_builders.get(report_type)
        lines = builder(students, include_header, include_summary, sort_by) if builder else []
        report_text = "\n".join(lines)

        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, "w") as file:
                file.write(report_text)
            log_action("REPORT", f"Report saved to {output_file}")

        return report_text

    def export_data(self, students, fmt, filepath):
        exporters = {
            "json": self._export_json,
            "csv": self._export_csv,
        }
        result = exporters.get(fmt, self._export_pipe)(students)

        if filepath:
            with open(filepath, "w") as file:
                file.write(result)
        return result

    def get_statistics(self, students):
        if not students:
            return {}

        gpas = [student.gpa for student in students if student.gpa is not None]
        grade_counts = self._count_grades(students)
        warning_count = sum(1 for student in students if student.warning)
        scholarship_count = sum(1 for student in students if student.scholarship_eligible)
        passing_count = sum(grade_counts[grade] for grade in ("A", "B", "C", "D"))

        return {
            "total": len(students),
            "avg_gpa": round(calculate_average(gpas), 2),
            "highest_gpa": round(max(gpas) if gpas else 0, 2),
            "lowest_gpa": round(min(gpas) if gpas else 0, 2),
            "grade_a": grade_counts["A"],
            "grade_b": grade_counts["B"],
            "grade_c": grade_counts["C"],
            "grade_d": grade_counts["D"],
            "grade_f": grade_counts["F"],
            "warnings": warning_count,
            "scholarship_eligible": scholarship_count,
            "pass_rate": round(passing_count / len(students) * 100, 1),
        }

    def search_students(self, query, field):
        query = str(query).lower()
        search_fields = {
            "name": lambda student: query in student.name.lower(),
            "major": lambda student: query in student.major.lower(),
            "id": lambda student: query == str(student.student_id),
        }
        matcher = search_fields.get(field)
        return [student for student in self.students if matcher and matcher(student)]

    def _build_grade_report(self, students, include_header, include_summary, sort_by):
        lines = self._build_header("STUDENT GRADES REPORT") if include_header else []
        for student in self._sort_students(students, sort_by):
            line = (
                f"  {format_name_for_report(student.name):<30} | "
                f"Grade: {student.final_grade or 'N/A':<3} | GPA: {student.gpa or 0:.2f}"
            )
            if student.scholarship_eligible:
                line += " | ★ SCHOLARSHIP"
            lines.append(line)

        if include_summary:
            lines.extend(self._build_grade_summary(students))
        return lines

    def _build_attendance_report(self, students, include_header, include_summary, sort_by):
        lines = self._build_header("STUDENT ATTENDANCE REPORT") if include_header else []
        for student in self._sort_students(students, sort_by):
            rate = calculate_attendance_rate(student.attendance_count)
            status_mark = "⚠️" if student.warning else "✓"
            lines.append(
                f"  {format_name_for_report(student.name):<30} | "
                f"Attended: {student.attendance_count}/{TOTAL_CLASSES} ({rate:.0f}%) {status_mark}"
            )

        if include_summary:
            lines.extend(self._build_attendance_summary(students))
        return lines

    def _build_full_report(self, students, include_header, include_summary, sort_by):
        lines = self._build_header("FULL STUDENT REPORT") if include_header else []
        for student in self._sort_students(students, sort_by):
            rate = calculate_attendance_rate(student.attendance_count)
            lines.extend(
                [
                    f"  {format_name_for_report(student.name)}",
                    f"    ID: {student.student_id} | Year: {student.year} | Major: {student.major}",
                    f"    Grade: {student.final_grade or 'N/A'} | GPA: {student.gpa or 0:.2f}",
                    f"    Attendance: {student.attendance_count}/{TOTAL_CLASSES} ({rate:.0f}%)",
                    f"    Status: {student.status}",
                ]
            )
            if student.notes:
                lines.append(f"    Notes: {'; '.join(student.notes)}")
            lines.append("")
        return lines

    def _build_header(self, title):
        return [
            "=" * REPORT_WIDTH,
            title,
            f"Generated: {current_timestamp()}",
            "=" * REPORT_WIDTH,
            "",
            ]

    def _build_grade_summary(self, students):
        grade_counts = self._count_grades(students)
        gpas = [student.gpa for student in students if student.gpa is not None]
        scholarship_count = sum(1 for student in students if student.scholarship_eligible)

        return [
            "",
            "-" * REPORT_WIDTH,
            f"  Total Students: {len(students)}",
            f"  Average GPA: {calculate_average(gpas):.2f}",
            "  Grade Distribution: "
            f"A={grade_counts['A']}, B={grade_counts['B']}, C={grade_counts['C']}, "
            f"D={grade_counts['D']}, F={grade_counts['F']}",
            f"  Scholarship Eligible: {scholarship_count}",
            ]

    def _build_attendance_summary(self, students):
        attendance_counts = [student.attendance_count for student in students]
        average_attendance = calculate_average(attendance_counts)
        warning_count = sum(1 for student in students if student.warning)

        return [
            "",
            "-" * REPORT_WIDTH,
            f"  Total Students: {len(students)}",
            f"  Average Attendance: {average_attendance:.1f}/{TOTAL_CLASSES} "
            f"({calculate_attendance_rate(average_attendance):.0f}%)",
            f"  Students with Warnings: {warning_count}",
            ]

    def _sort_students(self, students, sort_by):
        sort_options = {
            "name": lambda student: student.name,
            "grade": lambda student: student.gpa if student.gpa else 0,
            "attendance": lambda student: student.attendance_count,
            "id": lambda student: student.student_id,
        }
        key = sort_options.get(sort_by)
        reverse = sort_by in {"grade", "attendance"}
        return sorted(students, key=key, reverse=reverse) if key else students

    def _count_grades(self, students):
        grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for student in students:
            if student.final_grade in grade_counts:
                grade_counts[student.final_grade] += 1
        return grade_counts

    def _is_scholarship_eligible(self, student, average):
        return (
                average >= SCHOLARSHIP_MIN_AVERAGE
                and student.attendance_count >= SCHOLARSHIP_MIN_ATTENDANCE
        )

    def _send_notification(self, student, message, notification_type):
        if not validate_email(student.email):
            return

        self.notification_log.append(
            {
                "to": student.email,
                "message": message,
                "sent_at": current_timestamp(),
                "type": notification_type,
            }
        )

        if notification_type == "attendance":
            details = f"Attendance warning sent to {student.email}"
        else:
            details = f"{notification_type.title()} notification sent to {student.email}"
        log_action("NOTIFICATION", details)

    def _count_processed(self):
        self.processed_count += 1

    def _export_json(self, students):
        data = [
            {
                "name": student.name,
                "student_id": student.student_id,
                "email": student.email,
                "final_grade": student.final_grade,
                "gpa": student.gpa,
                "attendance_count": student.attendance_count,
                "warning": student.warning,
                "status": student.status,
                "scholarship_eligible": student.scholarship_eligible,
            }
            for student in students
        ]
        return json.dumps(data, indent=2)

    def _export_csv(self, students):
        rows = ["name,student_id,email,final_grade,gpa,attendance,warning,status"]
        rows.extend(
            f"{student.name},{student.student_id},{student.email},{student.final_grade},"
            f"{student.gpa},{student.attendance_count},{student.warning},{student.status}"
            for student in students
        )
        return "\n".join(rows) + "\n"

    def _export_pipe(self, students):
        return "".join(
            f"{student.name}|{student.student_id}|{student.final_grade}\n"
            for student in students
        )