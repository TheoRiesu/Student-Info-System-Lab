import random
import sqlite3

conn = sqlite3.connect('students_console.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        year INTEGER,
        random_id INTEGER,
        subjects TEXT
    )
''')
conn.commit()

while True:
    print("\n--- Menu ---")
    print("1. Add Student | 2. View Students | 3. Delete Student | 0. Exit")
    choice = input("Choice: ")
    
    if choice == '1':
        # Strings
        name = input("Enter Name: ") 
        course = input("Enter Course: ") 
        
        # List
        subjects = []
        print("Enter subjects one by one. Type '0' to stop.")
        while True:
            sub = input("Enter Subject: ")
            if sub == '0':
                break
            subjects.append(sub)
        
        # a incrementing count for unique stud id here
        cursor.execute("SELECT MAX(random_id) FROM students WHERE year = 2026")
        max_id = cursor.fetchone()[0]
        next_sequence = 1 if max_id is None else max_id + 1
        
        # Tuple
        student_id = (2026, next_sequence) 
        
        # Dictionary
        student_record = { 
            "Name": name, 
            "Course": course, 
            "ID": student_id, 
            "Subjects": subjects
        }

        subjects_str = ", ".join(student_record["Subjects"])
        cursor.execute("INSERT INTO students (name, course, year, random_id, subjects) VALUES (?, ?, ?, ?, ?)",
                       (student_record["Name"], student_record["Course"], student_record["ID"][0], student_record["ID"][1], subjects_str))
        conn.commit()
        
        print("Student added successfully!")
        
    elif choice == '2':
        print("\n--- Student Records ---")
        
        cursor.execute("SELECT * FROM students")
        db_records = cursor.fetchall()
        
        if not db_records:
            print("No records found in database.")
        
        for record in db_records:
            print(f"ID: {record[3]}-{record[4]}")
            print(f"Name: {record[1]} | Course: {record[2]}")
            print(f"Subjects: {record[5]}")
            print("-" * 20)
            
    elif choice == '3':
        print("\n--- Delete Student ---")
        student_id_input = input("Enter Student ID to delete (e.g., 2026-1) or '0' to cancel: ")
        
        if student_id_input == '0':
            continue
            
        try:
            year, random_id = map(int, student_id_input.split('-'))
            # check if meron before deleting
            cursor.execute("SELECT name FROM students WHERE year = ? AND random_id = ?", (year, random_id))
            student = cursor.fetchone()
            
            if student:
                cursor.execute("DELETE FROM students WHERE year = ? AND random_id = ?", (year, random_id))
                conn.commit()
                print(f"Student '{student[0]}' (ID: {student_id_input}) deleted successfully.")
            else:
                print("Error: Student ID not found.")
        except ValueError:
            print("Invalid format. Please use the format YYYY-ID (e.g., 2026-1).")

    elif choice == '0':
        print("Thank you")
        conn.close()
        break
    
    else:
        print("Invalid choice. Please try again.")