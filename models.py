from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Student:
    name: str
    student_id: int
    email: str
    grades: List[int]
    attendance_count: int
    year: int
    major: str
    phone: str
    address: str
    emergency_contact: str
    enrollment_date: str
    is_international: bool
    final_grade: Optional[str] = None
    gpa: Optional[float] = None
    warning: bool = False
    status: str = "active"
    notes: List[str] = field(default_factory=list)
    scholarship_eligible: bool = False

    def to_string(self):
        return self.name + " (" + str(self.student_id) + ")"

    def to_dict(self):
        return {
            "name": self.name,
            "student_id": self.student_id,
            "email": self.email,
            "grades": self.grades,
            "attendance_count": self.attendance_count,
            "year": self.year,
            "major": self.major,
            "phone": self.phone,
            "address": self.address,
            "emergency_contact": self.emergency_contact,
            "enrollment_date": self.enrollment_date,
            "is_international": self.is_international,
            "final_grade": self.final_grade,
            "gpa": self.gpa,
            "warning": self.warning,
            "status": self.status,
        }

    def is_equal(self, other):
        if other is None:
            return False
        return self.student_id == other.student_id

    def get_full_info(self):
        info = "Student: " + self.name + "\n"
        info += "ID: " + str(self.student_id) + "\n"
        info += "Email: " + self.email + "\n"
        info += "Year: " + str(self.year) + "\n"
        info += "Major: " + self.major + "\n"
        info += "Phone: " + self.phone + "\n"
        info += "Address: " + self.address + "\n"
        info += "Emergency: " + self.emergency_contact + "\n"
        return info

    def calculate_credits(self):
        credits_by_year = {
            1: 30,
            2: 60,
            3: 90,
            4: 120,
        }
        return credits_by_year.get(self.year, 0)