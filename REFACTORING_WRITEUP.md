# Refactoring Write-Up

## Overview

This assignment refactored a Python student grade management system. The goal was to improve code quality, readability, maintainability, and organization without changing the program's functional behavior.

The original program was run before refactoring and saved in `before_refactor.txt`. After refactoring, the program was run again and saved in `after_refactor.txt`. The outputs were compared. The only differences were timestamps, which are expected because the program generates the current time during each run.

## Code Smells Found

### Long Method

The original `process_students()` method handled grades, attendance, and status updates through a mode parameter. This made one method responsible for several different tasks.

### Large Class

`StudentManager` had many responsibilities, including processing grades, checking attendance, updating statuses, sending notifications, generating reports, exporting data, searching, and calculating statistics.

### Duplicate Code

The original code repeated logic for calculations, notifications, sorting, report formatting, and grade counting.

### Magic Numbers

Values such as `40`, `25`, `85`, and `35` were used directly in the code. These were replaced with named constants so their meaning is clearer.

### Long Parameter List

Some functions accepted many parameters, which made the code harder to read and easier to call incorrectly.

## Refactoring Changes Made

- Converted `Student` to a dataclass.
- Added clearer model methods such as `__str__`, `__eq__`, and `__hash__`.
- Split grade, attendance, and status processing into separate methods.
- Kept `process_students()` as a backward-compatible wrapper.
- Extracted shared calculations into utility functions.
- Replaced magic numbers with named constants.
- Simplified notification logic.
- Split report-building logic into smaller helper methods.
- Refactored `main.py` into clearer helper functions for printing headers, reports, statistics, notifications, and completion messages.

## Behavior Preservation

The program was run before and after refactoring. The outputs showed the same students, grades, GPA values, attendance values, warnings, statistics, notifications, and total operations. The only differences were timestamps, which are expected because timestamps are generated at runtime.

## Result

The refactored code is easier to read, easier to maintain, and better organized. The changes reduce code smells while preserving the original behavior of the program.