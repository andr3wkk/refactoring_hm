cat > REFACTORING_WRITEUP.md <<'EOF'
# Refactoring Write-Up

## Overview

This assignment refactored a Python student grade management system. The goal was to improve code quality, readability, maintainability, and organization without changing the program's functional behavior.

The original program was run before refactoring and saved in `before_refactor.txt`. After refactoring, the program was run again and saved in `after_refactor.txt`. The outputs were compared. The only differences were timestamps, which are expected because the program generates the current time during each run.

## Code Smells Found

### 1. Long Method

The original `process_students()` method handled several different tasks depending on the selected mode. It processed grades, attendance, and student statuses in one method. This made the method harder to read, test, and maintain.

### 2. Large Class

`StudentManager` had too many responsibilities. It handled grade processing, attendance processing, status updates, notifications, reports, statistics, searching, and exporting. This reduced cohesion because one class was responsible for many different types of behavior.

### 3. Long Parameter List

Some methods had many parameters, especially `process_students()` and `generate_report()`. Long parameter lists make code harder to understand and easier to call incorrectly.

### 4. Duplicate Code

There was repeated logic for formatting reports, calculating averages, handling notifications, sorting students, and counting grade distributions.

### 5. Magic Numbers

Numbers such as `40`, `25`, `85`, and `35` were used directly in the code. These values represented concepts such as total classes, GPA conversion, and scholarship requirements, but their meaning was not immediately clear.

### 6. Speculative or Unused Code

Some parts of the code existed for possible future use but were not needed by the current program. For example, the unused cache field in `StudentManager` added unnecessary complexity.

## Refactoring Changes Made

### 1. Converted Student to a Dataclass

The `Student` class was changed to use Python's `@dataclass`. This reduced boilerplate code and made the model easier to read while preserving the same student fields and behavior.

### 2. Split Grade, Attendance, and Status Logic

The original mode-based `process_students()` logic was separated into clearer methods:

- `process_grades()`
- `process_attendance()`
- `update_statuses()`

The original `process_students()` method was kept as a wrapper for backward compatibility.

### 3. Extracted Utility Functions

Common calculations and formatting logic were moved into `utils.py`, including:

- `calculate_average()`
- `calculate_gpa()`
- `calculate_attendance_rate()`
- `current_timestamp()`
- name formatting helpers

### 4. Replaced Magic Numbers with Constants

Important values were moved into named constants:

- `TOTAL_CLASSES`
- `GPA_DIVISOR`
- `SCHOLARSHIP_MIN_AVERAGE`
- `SCHOLARSHIP_MIN_ATTENDANCE`
- `REPORT_WIDTH`

This makes the code easier to understand and easier to change later.

### 5. Simplified Report Generation

Report generation was split into smaller helper methods for grade reports, attendance reports, full reports, headers, summaries, sorting, and grade counting.

### 6. Simplified Notification Logic

Repeated notification logic was moved into one helper method, `_send_notification()`. This reduces duplication and keeps notification formatting in one place.

### 7. Updated Main Program Calls

`main.py` now calls the clearer methods directly instead of relying on string modes:

- `manager.process_grades(...)`
- `manager.process_attendance(...)`
- `manager.update_statuses()`

## Behavior Preservation

The program was run before and after refactoring. The before and after outputs showed the same students, grades, GPA values, attendance values, warnings, statistics, notifications, and total operations. The only differences were timestamps, which are expected because timestamps are generated at runtime.

## Result

The refactored code is easier to read, easier to maintain, and better organized. The changes reduce code smells such as long methods, large classes, duplicate code, magic numbers, and poor cohesion while preserving the original program behavior.
EOF