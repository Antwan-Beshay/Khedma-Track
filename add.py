import sqlite3

connect = sqlite3.connect("database.db")
cursor = connect.cursor()

# حذف البيانات القديمة (اختياري)
cursor.execute("DELETE FROM coursess")

courses_data = [
    # Saturday
    ("3rd Preparatory Girls' Scouts", "Saturday", "10:00", "13:00", "bi bi-compass"),
    ("Joint Theater", "Saturday", "10:00", "13:00", "bi bi-theater-masks"),
    ("Joint Media", "Saturday", "13:00", "15:00", "bi bi-camera-reels"),
    ("Joint Programming & Computer", "Saturday", "15:00", "17:00", "bi bi-code-slash"),
    ("Joint Coptic", "Saturday", "17:00", "19:00", "bi bi-translate"),
    ("Joint Theater", "Saturday", "18:00", "21:00", "bi bi-theater-masks"),
    ("Joint Choir", "Saturday", "19:00", "21:00", "bi bi-music-note-list"),

    # Sunday
    ("1st & 2nd Preparatory Girls' Scouts", "Sunday", "10:30", "13:30", "bi bi-compass"),
    ("Joint Academic & Memorization", "Sunday", "15:20", "21:00", "bi bi-brain"),
    ("Joint Literature & Culture (Research)", "Sunday", "15:20", "21:00", "bi bi-book-half"),

    # Monday
    ("Joint Theater", "Monday", "15:00", "18:00", "bi bi-theater-masks"),
    ("Joint Engineering Innovations", "Monday", "17:00", "19:00", "bi bi-lightbulb"),
    ("Joint Theater", "Monday", "18:00", "21:00", "bi bi-theater-masks"),
    ("Joint Fine Arts", "Monday", "19:00", "21:00", "bi bi-brush"),

    # Tuesday
    ("Joint Academic", "Tuesday", "17:00", "19:00", "bi bi-mortarboard"),
    ("Joint Engineering Innovations", "Tuesday", "19:00", "21:00", "bi bi-lightbulb"),
    ("1st & 2nd Preparatory Boys' Scouts", "Tuesday", "19:00", "21:00", "bi bi-compass"),
    ("3rd Preparatory Boys' Scouts", "Tuesday", "19:00", "21:00", "bi bi-compass"),
    ("3rd Preparatory Girls' Scouts", "Tuesday", "19:00", "21:00", "bi bi-compass"),
    ("Girls' Chess", "Tuesday", "19:00", "21:00", "bi bi-trophy"),

    # Wednesday
    ("Joint Theater", "Wednesday", "12:00", "15:00", "bi bi-theater-masks"),
    ("Joint Theater", "Wednesday", "18:00", "21:00", "bi bi-theater-masks"),
    ("Joint Choir", "Wednesday", "18:30", "21:00", "bi bi-music-note-list"),
    ("Joint Literature & Culture (Research)", "Wednesday", "19:00", "21:00", "bi bi-book-half"),

    # Thursday
    ("Joint Hymns", "Thursday", "13:00", "15:00", "bi bi-music-note"),
    ("School of Deacons", "Thursday", "16:30", "18:00", "bi bi-heart"),
    ("1st & 2nd Preparatory Boys' Scouts", "Thursday", "19:00", "21:00", "bi bi-compass"),
    ("1st & 2nd Preparatory Girls' Scouts", "Thursday", "19:00", "21:00", "bi bi-compass"),

    # Friday
    ("Joint Coptic", "Friday", "09:00", "11:00", "bi bi-translate"),
    ("Girls' Chess", "Friday", "17:00", "19:00", "bi bi-trophy"),
    ("Girls' Chess", "Friday", "19:00", "21:00", "bi bi-trophy"),
    ("Joint Fine Arts", "Friday", "19:00", "21:00", "bi bi-brush"),
]

cursor.executemany(
    """
    INSERT INTO coursess (Name, day, start_time, end_time, icon)
    VALUES (?, ?, ?, ?, ?)
    """,
    courses_data,
)

connect.commit()
connect.close()

print("Courses inserted successfully.")