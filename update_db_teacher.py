import sqlite3

conn = sqlite3.connect("school.db")
c = conn.cursor()

# pievienosim jaunu kolonnu "full_name" tabulai "users"
c.execute("ALTER TABLE users ADD COLUMN full_name TEXT")

# aizpildīsim UPDATE, lai iestatītu "full_name" vērtību skolotājiem, kuriem tā vēl nav iestatīta
c.execute("""
UPDATE users
SET full_name = 'Skolotājs Demo'
WHERE role = 'teacher' AND full_name IS NULL
""")

conn.commit()
conn.close()

print("✅ full_name pievienots")