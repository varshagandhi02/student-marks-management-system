import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# DB setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll TEXT PRIMARY KEY,
            name TEXT,
            marks1 INTEGER,
            marks2 INTEGER,
            marks3 INTEGER,
            total INTEGER,
            average REAL,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def calculate_grade(m1, m2, m3):
    total = m1 + m2 + m3
    avg = total / 3
    grade = "A" if avg >= 90 else "B" if avg >= 75 else "C" if avg >= 60 else "D"
    return total, avg, grade

# Insert function
def add_student():
    roll = roll_var.get()
    name = name_var.get()
    try:
        m1 = int(marks1_var.get())
        m2 = int(marks2_var.get())
        m3 = int(marks3_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Marks must be integers")
        return

    total, avg, grade = calculate_grade(m1, m2, m3)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (roll, name, m1, m2, m3, total, avg, grade))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        fetch_data()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")
    conn.close()

def fetch_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    table.delete(*table.get_children())
    for row in rows:
        table.insert('', 'end', values=row)
    conn.close()

def delete_student():
    selected = table.focus()
    if selected:
        data = table.item(selected)
        roll = data['values'][0]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Deleted", "Student deleted successfully!")
    else:
        messagebox.showwarning("Select", "Please select a student")

# GUI
init_db()
root = tk.Tk()
root.title("Student Result Management System")
root.geometry("800x600")

# Variables
roll_var = tk.StringVar()
name_var = tk.StringVar()
marks1_var = tk.StringVar()
marks2_var = tk.StringVar()
marks3_var = tk.StringVar()

tk.Label(root, text="Roll No").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=roll_var).grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=name_var).grid(row=1, column=1)

tk.Label(root, text="Marks 1").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=marks1_var).grid(row=2, column=1)

tk.Label(root, text="Marks 2").grid(row=3, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=marks2_var).grid(row=3, column=1)

tk.Label(root, text="Marks 3").grid(row=4, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=marks3_var).grid(row=4, column=1)

tk.Button(root, text="Add Student", command=add_student).grid(row=5, column=0, columnspan=2, pady=10)

# Table
columns = ("Roll", "Name", "M1", "M2", "M3", "Total", "Average", "Grade")
table = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=80)

table.grid(row=6, column=0, columnspan=3, padx=20, pady=20)

tk.Button(root, text="Delete Selected", command=delete_student).grid(row=7, column=0, columnspan=2)

fetch_data()
root.mainloop()
