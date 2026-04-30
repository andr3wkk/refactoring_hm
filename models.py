# models.py - Student data models
# This file contains all the data structures for the system
# Author: [Original Developer]
# Date: 2024-01-15
# Modified: 2024-03-20, 2024-05-11, 2024-06-03, 2024-09-17

class Student:
    def __init__(self, name, student_id, email, grades, attendance_count,
                 year, major, phone, address, emergency_contact,
                 enrollment_date, is_international):
        self.name = name
        self.student_id = student_id
        self.email = email
        self.grades = grades
        self.attendance_count = attendance_count
        self.year = year
        self.major = major
        self.phone = phone
        self.address = address
        self.emergency_contact = emergency_contact
        self.enrollment_date = enrollment_date
        self.is_international = is_international
        self.final_grade = None
        self.gpa = None
        self.warning = False
        self.status = "active"
        self.notes = []
        self.scholarship_eligible = False
        # TODO: add support for multiple semesters
        # TODO: add GPA history tracking
        # TODO: integrate with university API

    # This method converts student to a string
    def to_string(self):
        return self.name + " (" + str(self.student_id) + ")"

    # This method converts student to a dictionary
    def to_dict(self):
        d = {}
        d["name"] = self.name
        d["student_id"] = self.student_id
        d["email"] = self.email
        d["grades"] = self.grades
        d["attendance_count"] = self.attendance_count
        d["year"] = self.year
        d["major"] = self.major
        d["phone"] = self.phone
        d["address"] = self.address
        d["emergency_contact"] = self.emergency_contact
        d["enrollment_date"] = self.enrollment_date
        d["is_international"] = self.is_international
        d["final_grade"] = self.final_grade
        d["gpa"] = self.gpa
        d["warning"] = self.warning
        d["status"] = self.status
        return d

    # This method checks if two students are equal
    def is_equal(self, other):
        if other is None:
            return False
        return self.student_id == other.student_id

    # Legacy method - kept for backward compatibility
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

    # Never used but might be needed later
    def calculate_credits(self):
        if self.year == 1:
            return 30
        elif self.year == 2:
            return 60
        elif self.year == 3:
            return 90
        elif self.year == 4:
            return 120
        else:
            return 0

    # Experimental feature - not yet implemented
    def predict_graduation(self):
        pass
