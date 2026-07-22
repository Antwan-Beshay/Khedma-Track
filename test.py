import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
SELECT status, COUNT(*)
FROM attendance
GROUP BY status
""")

print(cursor.fetchall())

conn.close()