# Student Information System — Documentation

### Stack

- **Language:** Python 3.x
- **GUI Toolkit:** Tkinter (ttk)
- **Database:** SQLite (built-in)
- **Last Updated:** August 2026

---

## 1. Project Layout

```
Student-Info-System-Lab/
├── Lab2.py          # Console-based interface (CLI)
├── gui.py           # Graphical interface (Tkinter)
├── students_console.db  # SQLite database (auto-created)
├── README.md        # User guide and overview
├── DOCUMENTATION.md # This detailed documentation
└── CHANGELOG.md     # Version history
```

---

## 2. Environment & Setup

### Prerequisites

- Python 3.x (includes SQLite3 module)
- No external dependencies required for Lab2.py
- Tkinter must be enabled for gui.py (`sudo apt-get install python3-tk` on Ubuntu/Debian)

### Running the Applications

**Console Interface:**

```bash
python3 Lab2.py
```

**Graphical Interface:**

```bash
python3 gui.py
```

### Database Initialization

Both applications auto-create the SQLite database on first run:

- File: `main.db` (console) or persists alongside `gui.py`
- Table: `students` with automatic schema creation via `CREATE TABLE IF NOT EXISTS`

---

## 3. Core Engine

### 3.1 Students Table Schema

| Column      | Type    | Description                               |
| ----------- | ------- | ----------------------------------------- |
| `id`        | INTEGER | Auto-increment primary key                |
| `name`      | TEXT    | Student's full name                       |
| `course`    | TEXT    | Academic program/course                   |
| `year`      | INTEGER | Enrollment year                           |
| `random_id` | INTEGER | Unique sequence number                    |
| `subjects`  | TEXT    | Comma-separated list of enrolled subjects |

### 3.2 ID Format

Student IDs use the format: `YYYY-ID`

- **Example:** `2026-1` means year 2026, random_id 1
- Generated automatically when adding a new student
- Used for deletion and subject management

### 3.3 Data Flow

**Add Student:**

1. Enter name and course
2. Enter subjects one by one (type '0' to stop)
3. System generates unique ID
4. Record inserted into SQLite database

**View Students:**

1. Query all records from `students` table
2. Display in formatted output with ID, name, course, and subjects

**Delete Student:**

1. Enter Student ID in `YYYY-ID` format
2. System validates ID exists in database
3. Record deleted with confirmation

**Manage Enrolled Subjects:**

1. Enter Student ID in `YYYY-ID` format
2. View current enrolled subjects
3. Add new subject (with duplicate check)
4. Remove existing subject (with enrollment check)
5. Changes saved back to database

---

## 4. Graphical Interface (gui.py)

### 4.1 Main Window

- **Title:** "Student Information Management System"
- **Size:** 900x850 pixels
- **Resizable:** Fixed (cannot resize)

### 4.2 Input Fields

| Field                         | Purpose                                     |
| ----------------------------- | ------------------------------------------- |
| Name                          | Student's full name                         |
| Course                        | Academic program                            |
| Subject                       | Individual subject entry (Add Student mode) |
| Student ID to Delete          | Format: YYYY-ID                             |
| Student ID to Manage Subjects | Format: YYYY-ID                             |

### 4.3 Functional Areas

**Enrolled Subjects Frame:**

- Add Subject button + text field
- Remove Subject button
- Listbox displaying enrolled subjects

**Student Records Table:**

- Treeview table showing all students
- Columns: ID, Name, Course, Subjects
- Clicking a row automatically populates ID fields

**Button Frame:**

- Add Student
- Clear Fields
- Delete Student
- Manage Subjects
- Exit

### 4.4 Special Features

**Row Click Functionality:**

- Clicking any row in the Student Records table
- Automatically populates both "Student ID to Delete" and "Student ID to Manage Subjects" fields
- Overwrites any existing content in the fields

**Manage Subjects Modal:**

- Opens as a Toplevel window
- Displays current subjects in a listbox
- Add subject: enters new subject name, validates no duplicates
- Remove subject: selects from listbox and removes
- Save & Close: saves changes to database AND refreshes main student table

**Subject Textfield Position:**

- In the manage subjects modal, the subject input field appears
- Above the "Add Subject" and "Remove Subject" buttons
- Below the subjects listbox

### 4.5 Event Handling

**<ButtonRelease-1> on Student Table:**

- `on_row_click(event)` function binds to table clicks
- Retrieves selected row values
- Sets `student_id_var` and `student_id_manage_var` text fields
- Useful for quickly selecting a student for deletion or subject management

---

## 5. Usage Examples

### Adding a Student (Console)

```
--- Menu ---
1. Add Student | 2. View Students | 3. Delete Student | 4. Manage Enrolled Subjects | 0. Exit
Choice: 1

Enter Name: John Doe
Enter Course: Computer Science

Enter subjects one by one. Type '0' to stop.
Enter Subject: Mathematics
Enter Subject: Physics
Enter Subject: Chemistry
Enter Subject: 0

Student added successfully!
```

### Managing Subjects (Console)

```
--- Menu ---
1. Add Student | 2. View Students | 3. Delete Student | 4. Manage Enrolled Subjects | 0. Exit
Choice: 4

Enter Student ID to manage subjects (e.g., 2026-1) or '0' to cancel: 2026-1

Student: John Doe
Current subjects: Mathematics, Physics

1. Add subject
2. Remove subject
3. Back to main menu
Choice: 1

Enter subject to add: Chemistry

Subject 'Chemistry' added successfully.

Current subjects: Mathematics, Physics, Chemistry
```

### Using the GUI

1. Run `python3 gui.py`
2. The main window appears with input fields and student table
3. Enter student details and click "Add Student"
4. Click on any row in the table to select a student
5. Use "Manage Subjects" to add/remove subjects for the selected student
6. Click "Delete Student" to remove a selected student

---

## 6. Troubleshooting

### Common Issues

**Tkinter not available:**

- Error: `ModuleNotFoundError: No module named 'tkinter'`
- Solution: Install tkinter package (`sudo apt-get install python3-tk`)

**Database locked error:**

- Ensure only one instance of the application is running
- Close any other programs using `students_console.db`

**Invalid Student ID format:**

- Use format `YYYY-ID` (e.g., `2026-1`)
- Ensure year matches the academic year in the system

**Subject already enrolled:**

- When adding a subject, duplicates are checked
- System will show message if subject already exists

### Refreshing Data

After managing subjects, the main student table automatically refreshes to reflect changes.
After deleting a student, the table also refreshes.

---

## 7. License

MIT License — see [LICENSE](./LICENSE) for details.

---
