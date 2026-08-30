import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

conn = sqlite3.connect("main.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        year INTEGER,
        random_id INTEGER,
        subjects TEXT
    )
""")

conn.commit()

root = tk.Tk()
root.title("Student Information Management System")
root.geometry("900x850")
root.resizable(False, False)

name_var = tk.StringVar()
course_var = tk.StringVar()
subject_var = tk.StringVar()
student_id_var = tk.StringVar()
student_id_manage_var = tk.StringVar()

subjects = []


def add_subject():
    subject = subject_var.get().strip()

    if subject == "":
        messagebox.showwarning(
            "Missing Subject",
            "Please enter a subject."
        )
        return

    subjects.append(subject)
    subject_listbox.insert(tk.END, subject)
    subject_var.set("")


def remove_subject():
    selected = subject_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a subject to remove."
        )
        return

    index = selected[0]
    subjects.pop(index)
    subject_listbox.delete(index)


def generate_student_id():
    cursor.execute(
        "SELECT MAX(random_id) FROM students WHERE year = 2026"
    )

    max_id = cursor.fetchone()[0]
    next_sequence = 1 if max_id is None else max_id + 1

    return (2026, next_sequence)


def add_student():
    name = name_var.get().strip()
    course = course_var.get().strip()

    if name == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter the student's name."
        )
        return

    if course == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter the student's course."
        )
        return

    if not subjects:
        messagebox.showwarning(
            "Missing Subjects",
            "Please add at least one subject."
        )
        return

    student_id = generate_student_id()

    student_record = {
        "Name": name,
        "Course": course,
        "ID": student_id,
        "Subjects": subjects.copy()
    }

    subjects_str = ", ".join(student_record["Subjects"])

    cursor.execute("""
        INSERT INTO students
        (name, course, year, random_id, subjects)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_record["Name"],
        student_record["Course"],
        student_record["ID"][0],
        student_record["ID"][1],
        subjects_str
    ))

    conn.commit()

    messagebox.showinfo(
        "Success",
        f"Student added successfully!\n\n"
        f"Student ID: {student_id[0]}-{student_id[1]}"
    )

    clear_fields()
    load_students()


def load_students():
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    for record in records:
        student_id = f"{record[3]}-{record[4]}"

        student_table.insert(
            "",
            tk.END,
            values=(
                student_id,
                record[1],
                record[2],
                record[5]
            )
        )


def delete_student():
    student_id_input = student_id_var.get().strip()

    if student_id_input == "":
        messagebox.showwarning(
            "Missing Student ID",
            "Please enter a Student ID."
        )
        return

    try:
        year, random_id = map(
            int,
            student_id_input.split("-")
        )

        cursor.execute(
            """
            SELECT name
            FROM students
            WHERE year = ? AND random_id = ?
            """,
            (year, random_id)
        )

        student = cursor.fetchone()

        if student:
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete '{student[0]}'?"
            )

            if not confirm:
                return

            cursor.execute(
                """
                DELETE FROM students
                WHERE year = ? AND random_id = ?
                """,
                (year, random_id)
            )

            conn.commit()

            messagebox.showinfo(
                "Deleted",
                f"Student '{student[0]}' "
                f"has been deleted successfully."
            )

            student_id_var.set("")
            load_students()

        else:
            messagebox.showerror(
                "Student Not Found",
                "Student ID not found."
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Format",
            "Please use the format YYYY-ID.\n\n"
            "Example: 2026-1"
        )


def clear_fields():
    name_var.set("")
    course_var.set("")
    subject_var.set("")
    student_id_var.set("")

    subjects.clear()
    subject_listbox.delete(0, tk.END)


def manage_subjects():
    student_id_input = student_id_manage_var.get().strip()

    if student_id_input == "":
        messagebox.showwarning(
            "Missing Student ID",
            "Please enter a Student ID."
        )
        return

    try:
        year, random_id = map(
            int,
            student_id_input.split("-")
        )

        cursor.execute(
            """
            SELECT name, subjects
            FROM students
            WHERE year = ? AND random_id = ?
            """,
            (year, random_id)
        )

        student = cursor.fetchone()

        if not student:
            messagebox.showerror(
                "Student Not Found",
                "Student ID not found."
            )
            return

        current_subjects = (student[1] or "").split(", ") if student[1] else []

        subject_win = tk.Toplevel(root)
        subject_win.title(f"Manage Subjects - {student[0]}")
        subject_win.geometry("400x400")
        subject_win.resizable(False, False)

        tk.Label(
            subject_win,
            text=f"Student: {student[0]}",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Label(
            subject_win,
            text="Current Subjects:"
        ).pack(anchor="w", padx=20)

        listbox = tk.Listbox(subject_win, width=40, height=8)
        listbox.pack(padx=20, pady=5)

        for s in current_subjects:
            listbox.insert(tk.END, s)

        subject_new_var = tk.StringVar()
        tk.Entry(
            subject_win,
            textvariable=subject_new_var,
            width=30
        ).pack(padx=20, pady=5)

        def add_subject():
            new_sub = subject_new_var.get().strip()
            if new_sub == "":
                messagebox.showwarning(
                    "Missing Subject",
                    "Please enter a subject."
                )
                return
            if new_sub not in current_subjects:
                current_subjects.append(new_sub)
                listbox.insert(tk.END, new_sub)
                subject_new_var.set("")
            else:
                messagebox.showinfo(
                    "Already Enrolled",
                    f"'{new_sub}' is already enrolled."
                )

        def remove_subject():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning(
                    "No Selection",
                    "Please select a subject to remove."
                )
                return
            index = selected[0]
            removed = current_subjects.pop(index)
            listbox.delete(index)
            messagebox.showinfo(
                "Removed",
                f"'{removed}' has been removed."
        )

        btn_frame = tk.Frame(subject_win)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Subject",
            command=add_subject
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Remove Subject",
            command=remove_subject
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            subject_win,
            text="Save & Close",
            command=lambda: [save_subjects(student[0], year, random_id, current_subjects), subject_win.destroy(), load_students()]
        ).pack(pady=10)

    except ValueError:
        messagebox.showerror(
            "Invalid Format",
            "Please use the format YYYY-ID.\n\n"
            "Example: 2026-1"
        )


def save_subjects(name, year, random_id, subjects):
    subjects_str = ", ".join(subjects) if subjects else ""
    cursor.execute(
        """
        UPDATE students
        SET subjects = ?
        WHERE year = ? AND random_id = ?
        """,
        (subjects_str, year, random_id)
    )
    conn.commit()
    messagebox.showinfo(
        "Saved",
        f"Subjects for {name} have been updated."
    )


def close_program():
    conn.close()
    root.destroy()


title_label = tk.Label(
    root,
    text="Student Information Management System",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=15)

info_frame = tk.LabelFrame(
    root,
    text="Student Information",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

info_frame.pack(
    padx=20,
    fill="x"
)

tk.Label(
    info_frame,
    text="Name:"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=5,
    pady=5
)

name_entry = tk.Entry(
    info_frame,
    textvariable=name_var,
    width=40
)

name_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

tk.Label(
    info_frame,
    text="Program:"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=5,
    pady=5
)

course_entry = tk.Entry(
    info_frame,
    textvariable=course_var,
    width=40
)

course_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

subject_frame = tk.LabelFrame(
    root,
    text="Enrolled Subjects",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

subject_frame.pack(
    padx=20,
    pady=10,
    fill="x"
)

subject_entry = tk.Entry(
    subject_frame,
    textvariable=subject_var,
    width=40
)

subject_entry.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

add_subject_button = tk.Button(
    subject_frame,
    text="Add Subject",
    command=add_subject
)

add_subject_button.grid(
    row=0,
    column=1,
    padx=5
)

remove_subject_button = tk.Button(
    subject_frame,
    text="Remove Subject",
    command=remove_subject
)

remove_subject_button.grid(
    row=0,
    column=2,
    padx=5
)

subject_listbox = tk.Listbox(
    subject_frame,
    width=65,
    height=5
)

subject_listbox.grid(
    row=1,
    column=0,
    columnspan=3,
    padx=5,
    pady=5
)

button_frame = tk.Frame(root)

button_frame.pack(pady=5)

add_button = tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=add_student
)

add_button.grid(
    row=0,
    column=0,
    padx=5
)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_fields
)

clear_button.grid(
    row=0,
    column=1,
    padx=5
)

records_frame = tk.LabelFrame(
    root,
    text="Student Records",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

records_frame.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

columns = (
    "ID",
    "Name",
    "Course",
    "Subjects"
)

student_table = ttk.Treeview(
    records_frame,
    columns=columns,
    show="headings",
    height=7
)

student_table.heading(
    "ID",
    text="Student ID"
)

student_table.heading(
    "Name",
    text="Name"
)

student_table.heading(
    "Course",
    text="Course"
)

student_table.heading(
    "Subjects",
    text="Subjects"
)

student_table.column(
    "ID",
    width=100
)

student_table.column(
    "Name",
    width=180
)

student_table.column(
    "Course",
    width=180
)

student_table.column(
    "Subjects",
    width=350
)

student_table.pack(
    fill="both",
    expand=True
)

delete_frame = tk.Frame(root)

delete_frame.pack(pady=5)

tk.Label(
    delete_frame,
    text="Student ID to Delete:"
).grid(
    row=0,
    column=0,
    padx=5
)

delete_entry = tk.Entry(
    delete_frame,
    textvariable=student_id_var,
    width=20
)

delete_entry.grid(
    row=0,
    column=1,
    padx=5
)

delete_button = tk.Button(
    delete_frame,
    text="Delete Student",
    command=delete_student
)

delete_button.grid(
    row=0,
    column=2,
    padx=5
)

def on_row_click(event):
    selected_item = student_table.selection()
    if selected_item:
        values = student_table.item(selected_item, "values")
        if values:
            student_id = values[0]
            student_id_var.set(student_id)
            student_id_manage_var.set(student_id)

student_table.bind("<ButtonRelease-1>", on_row_click)

manage_frame = tk.Frame(root)
manage_frame.pack(pady=5)

tk.Label(
    manage_frame,
    text="Student ID to Manage Subjects:"
).grid(
    row=0,
    column=0,
    padx=5
)

manage_entry = tk.Entry(
    manage_frame,
    textvariable=student_id_manage_var,
    width=20
)

manage_entry.grid(
    row=0,
    column=1,
    padx=5
)

manage_button = tk.Button(
    manage_frame,
    text="Manage Subjects",
    command=manage_subjects
)

manage_button.grid(
    row=0,
    column=2,
    padx=5
)

exit_button = tk.Button(
    root,
    text="Exit",
    width=15,
    command=close_program
)

exit_button.pack(pady=10)

load_students()

root.protocol(
    "WM_DELETE_WINDOW",
    close_program
)

root.mainloop()