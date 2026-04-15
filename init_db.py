import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("school.db")
c = conn.cursor()

# ===== USERS =====
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# ===== STUDENTS =====
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    class TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# ===== SUBJECTS =====
c.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# ===== GRADES =====
c.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade INTEGER,
    date TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")

# ===== USERS DATA =====
users = [
    ("anna", generate_password_hash("1234"), "student"),
    ("peter", generate_password_hash("1234"), "student"),
    ("teacher", generate_password_hash("teacher"), "teacher")
]

c.executemany(
    "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
    users
)

# ===== STUDENTS DATA =====
students = [
    ("Anna Ivanova", "10.A", 1),
    ("Peter Kalnynsh", "10.A", 2)
]

c.executemany(
    "INSERT INTO students (full_name, class, user_id) VALUES (?, ?, ?)",
    students
)

# ===== SUBJECTS DATA =====
subjects = [
    ("Matemātika",),
    ("Informatika",),
    ("Latviešu valoda",)
]

c.executemany(
    "INSERT INTO subjects (name) VALUES (?)",
    subjects
)

# ===== GRADES DATA =====
grades = [
    (1, 1, 9, "2026-02-10"),
    (1, 2, 10, "2026-02-12"),
    (1, 3, 8, "2026-02-14"),

    (2, 1, 7, "2026-02-10"),
    (2, 2, 8, "2026-02-12"),
    (2, 3, 9, "2026-02-14")
]

c.executemany(
    "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)",
    grades
)

conn.commit()
conn.close()

print("✅ Datubāze 'school.db' ir izveidota un aizpildīta ar sākotnējiem datiem.")