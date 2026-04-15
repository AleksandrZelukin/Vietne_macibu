import sqlite3

conn = sqlite3.connect("school.db")
c = conn.cursor()

# добавляем поле, если его ещё нет
c.execute("ALTER TABLE users ADD COLUMN full_name TEXT")

# заполним имя текущему учителю
c.execute("""
UPDATE users
SET full_name = 'Skolotājs Demo'
WHERE role = 'teacher' AND full_name IS NULL
""")

conn.commit()
conn.close()

print("✅ full_name pievienots")