# Student Information System Lab

> **📄 Documentation:** [DOCUMENTATION.md](./DOCUMENTATION.md)

## Description

A Student Information Management System built with Python and SQLite. This laboratory project demonstrates CRUD operations (Create, Read, Update, Delete) for student records with subject enrollment management.

---

## Features

- **Add Student:** Register new students with name, course, and enrolled subjects
- **View Students:** Display all student records with ID, name, course, and subjects
- **Delete Student:** Remove student records by Student ID (format: YYYY-ID)
- **Manage Enrolled Subjects:** Add or remove subjects for existing students
- **SQLite Backend:** Persistent storage with automatic schema creation

---

## Getting Started

### Prerequisites

- Python 3.x
- SQLite (built-in with Python)

### Running the Application

```bash
python3 Lab2.py
```

### Menu Options

| Option | Description                                                  |
| ------ | ------------------------------------------------------------ |
| `1`    | Add Student - Register a new student with subjects           |
| `2`    | View Students - Display all student records                  |
| `3`    | Delete Student - Remove a student by ID                      |
| `4`    | Manage Enrolled Subjects - Add/remove subjects for a student |
| `0`    | Exit - Close the application                                 |

---

## Student ID Format

Use the format `YYYY-ID` (e.g., `2026-1`) when deleting or managing subjects for a student.

The ID consists of:

- **Year:** The academic year (e.g., 2026)
- **Random ID:** A unique sequence number

---

## GUI Version

A graphical interface is also available:

```bash
python3 gui.py
```

The GUI provides:

- Visual student table with scrollable records
- Text fields for adding/deleting students
- Subject enrollment management with add/remove controls
- Row clicking to automatically populate ID fields
- Modal dialogs for managing enrolled subjects

---

## Technical Details

### Database Schema

```sql
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    year INTEGER,
    random_id INTEGER,
    subjects TEXT
)
```

- `subjects` stores comma-separated subject list
- Year and random_id combine to form the student ID

### Project Structure

```
Student-Info-System-Lab/
├── Lab2.py         # Console-based interface
├── gui.py          # Graphical interface (Tkinter)
├── students_console.db  # SQLite database
├── README.md       # This file
├── DOCUMENTATION.md  # Detailed documentation
└── CHANGELOG.md    # Version history
---
```
