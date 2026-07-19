import sqlite3

connect = sqlite3.connect("database.db")
cursor = connect.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


cursor.execute('CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT , fname TEXT NOT NULL , lname TEXT NOT NULL , uname TEXT NOT NULL UNIQUE , email text NOT NULL UNIQUE , password TEXT NOT NULL , img text NOT NULL DEFAULT "static/img/profile.png"  , role text  NOT NULL, qr text  , qr_token text  UNIQUE)')

cursor.execute('CREATE TABLE coursess (id INTEGER PRIMARY KEY AUTOINCREMENT,Name text NOT NULL , day text, start_time text , end_time text , icon text  ) ')

cursor.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    attendance_date TEXT NOT NULL,
    attendance_time TEXT NOT NULL,

    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(course_id) REFERENCES coursess(id)
)
""")

cursor.execute("""
CREATE TABLE write (
    title text NOT NULL , 
    content text NOT NULL, 
    img text ,
    teacher text NOT NULL 
    
)
    
""")



connect.commit()
connect.close()




