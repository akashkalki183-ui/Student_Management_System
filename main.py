from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import openpyxl
from tkinter import filedialog

# Create Database and Table
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    usn TEXT,
    course TEXT,
    phone TEXT
)
""")

conn.commit()
conn.close()


# Save Student
def save_student():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name, usn, course, phone) VALUES (?, ?, ?, ?)",
        (
            name_entry.get(),
            usn_entry.get(),
            course_entry.get(),
            phone_entry.get()
        )
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student Saved Successfully!")

    name_entry.delete(0, END)
    usn_entry.delete(0, END)
    course_entry.delete(0, END)
    phone_entry.delete(0, END)

def search_student():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE usn=?",
        (usn_entry.get(),)
    )

    row = cursor.fetchone()

    if row:
        name_entry.delete(0, END)
        course_entry.delete(0, END)
        phone_entry.delete(0, END)

        name_entry.insert(0, row[1])
        course_entry.insert(0, row[3])
        phone_entry.insert(0, row[4])
    else:
        messagebox.showerror("Error", "Student Not Found")

    conn.close()
def update_student():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, course=?, phone=?
        WHERE usn=?
    """, (
        name_entry.get(),
        course_entry.get(),
        phone_entry.get(),
        usn_entry.get()
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student Updated Successfully!")

def delete_student():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE usn=?",
        (usn_entry.get(),)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student Deleted Successfully!")

    name_entry.delete(0, END)
    usn_entry.delete(0, END)
    course_entry.delete(0, END)
    phone_entry.delete(0, END)

def view_students():
    view = Toplevel(root)
    view.title("All Students")
    view.geometry("700x400")

    tree = ttk.Treeview(
        view,
        columns=("ID", "Name", "USN", "Course", "Phone"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("USN", text="USN")
    tree.heading("Course", text="Course")
    tree.heading("Phone", text="Phone")

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")

    for row in cursor.fetchall():
        tree.insert("", END, values=row)

    conn.close()
    tree.pack(fill=BOTH, expand=True)

def export_to_excel():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Students"

    sheet.append(["ID", "Name", "USN", "Course", "Phone"])

    for row in rows:
        sheet.append(row)

    file = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel File", "*.xlsx")]
    )

    if file:
        workbook.save(file)
        messagebox.showinfo("Success", "Excel file exported successfully!")

    conn.close()

# Main Window

def login():
    if username_entry.get() == "admin" and password_entry.get() == "admin123":
        login_window.destroy()
        root.deiconify()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

root = Tk()
root.withdraw()
root.title("Student Management System")
root.geometry("700x500")
root.configure(bg="lightblue")

Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="lightblue",
    fg="blue"
).pack(pady=20)

Label(root, text="Student Name", bg="lightblue").pack()
name_entry = Entry(root, width=40)
name_entry.pack()

Label(root, text="USN", bg="lightblue").pack()
usn_entry = Entry(root, width=40)
usn_entry.pack()

Label(root, text="Course", bg="lightblue").pack()
course_entry = Entry(root, width=40)
course_entry.pack()

Label(root, text="Phone", bg="lightblue").pack()
phone_entry = Entry(root, width=40)
phone_entry.pack()

Button(
    root,
    text="Save Student",
    bg="green",
    fg="white",
    width=20,
    command=save_student
).pack(pady=20)

Button(
    root,
    text="Search Student",
    bg="orange",
    fg="white",
    width=20,
    command=search_student
).pack(pady=5)

Button(
    root,
    text="Update Student",
    bg="Purple",
    fg="white",
    width=20,
    command=update_student
).pack(pady=5)

Button(
    root,
    text="Delete Student",
    bg="Red",
    fg="white",
    width=20,
    command=delete_student
).pack(pady=5)

Button(
    root,
    text="View Students",
    bg="blue",
    fg="white",
    width=20,
    command=view_students
).pack(pady=10)

Button(
    root,
    text="Export to Excel",
    bg="darkgreen",
    fg="white",
    width=20,
    command=export_to_excel
).pack(pady=5)

Button(
    root,
    text="Exit",
    bg="gray",
    fg="white",
    width=20,
    command=root.destroy
).pack(pady=10)

login_window = Tk()
login_window.title("Login")
login_window.geometry("350x250")
login_window.configure(bg="lightblue")

Label(login_window, text="LOGIN", font=("Arial",18,"bold"), bg="lightblue").pack(pady=10)

Label(login_window, text="Username", bg="lightblue").pack()
username_entry = Entry(login_window)
username_entry.pack()

Label(login_window, text="Password", bg="lightblue").pack()
password_entry = Entry(login_window, show="*")
password_entry.pack()

Button(login_window,
       text="Login",
       command=login,
       bg="green",
       fg="white").pack(pady=15)

login_window.mainloop()



root.mainloop()