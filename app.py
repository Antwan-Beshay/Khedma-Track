from flask import Flask, flash, redirect , render_template , url_for , session , request
import sqlite3
import datetime
import secrets
from form import registerForm ,loginform
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from upload import postform
import smtplib
from email.mime.text import MIMEText
from email.header import Header


app = Flask(__name__)
app.config['SECRET_KEY'] = '11f92b122aeec0cdfa672a8e8f00f2c7ba29738f4da3f42f3d0db91b332e76083cd483d5052a5476dce5b9e728c8df8d94e64d28e0740192f0625c2750144849' 


def send_course_email(receiver_email, student_name, course_name, day, time):

    sender_email = "antwanbeshay260@gmail.com"
    app_password = "sgan xoca eogb bqdo"

    subject = "Reminder: Your class starts in 15 minutes"

    body = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="UTF-8">
    </head>

    <body style="font-family:Arial;background:#f5f5f5;padding:30px">

        <div style="max-width:600px;margin:auto;background:white;border-radius:12px;padding:30px">

            <h2 style="background:#0d6efd;color:white;padding:20px;text-align:center">
                📚 تذكير بموعد الحصة
            </h2>

            <p>مرحبًا <strong>{student_name}</strong></p>

            <p>نذكرك بأن حصتك ستبدأ بعد <strong>15 دقيقة</strong>.</p>

            <div style="background:#eef5ff;padding:15px;border-right:5px solid #0d6efd">

                <p><b>📖 المادة:</b> {course_name}</p>

                <p><b>📅 اليوم:</b> {day}</p>

                <p><b>🕒 الوقت:</b> {time}</p>

            </div>

            <br>

            <a href="http://127.0.0.1:5000/login"
               style="background:#0d6efd;color:white;padding:12px 22px;text-decoration:none;border-radius:8px;">
               فتح النظام
            </a>

        </div>

    </body>
    </html>
    """

    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

@app.route("/")
def load():
    return render_template("index.html" , title="Loading")
@app.route("/main")
def Main():
    return render_template("main.html", title="Main")





def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn




@app.route("/Login" , methods=["GET", "POST"] )
def login():
    
    fmesage = None
    form = loginform()
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM student WHERE  email= ? AND password = ?', 
                            (mail, password)).fetchone()
        conn.close()
        if user:
            # حفظ اسم المستخدم ونوعه في الجلسة
            session["email_sent"] = False
            session["notification_sent"] = False
            session['id'] = user['id']
            session['mail'] = user['email']
            session['role'] = user['role']
            session['fname'] = user['fname']
            session['lname'] = user['lname']
            session["username"] = user['uname']
            session["qr_token"] = user['qr_token']
            role = session['role']
            if role == "student" or  role == "Student" :
                return redirect(url_for("Dashboard"))
            else:
                return redirect(url_for("Teacher"))
                
        else:
            fmesage = "email or password is not correct."
            flash(fmesage, "danger")

    return render_template("login.html", title="Login", form=form ,message= fmesage )
    

@app.route("/register", methods=["GET", "POST"])
def register():
    token = secrets.token_urlsafe(32)
    form = registerForm()  
    fmessage = None
    
    if form.validate_on_submit():
        flash("Account created for {}!".format(form.uname.data), "success")
    
        try:
            conect = sqlite3.connect("database.db")
            cursor = conect.cursor()
            cursor.execute("insert into student (fname ,  lname , uname ,email, password, role , qr_token) Values(?, ?, ?, ?, ?, ?, ?)",(form.fname.data ,form.lname.data, form.uname.data ,form.email.data ,  form.password.data , form.role.data,token))
            conect.commit()
            student_id = cursor.lastrowid
            conect.close()
            session["email_sent"] = False
            session["notification_sent"] = False
            session["fname"] =  form.fname.data
            session["id"] = student_id 
            session["lname"]=  form.lname.data
            session["email"]= form.email.data
            session["username"] = form.uname.data
            role = form.role.data
            session["role"] = form.role.data
            session["qr_token"] =  token
            if role == "student" or  role == "Student" :
                return redirect(url_for("Dashboard"))
            else:
                return redirect(url_for("Teacher"))
        except sqlite3.IntegrityError :
            fmessage = 'Username or email already exists'
            flash(fmessage, "danger")
        finally:
            conect.close()
    if form.is_submitted() and not form.validate():
        fmessage = 'Please correct the errors in the form.'
        flash(fmessage, "danger")
    return render_template("register.html", title="Register", form=form , message= fmessage)


@app.route("/write", methods=["GET", "POST"])
def write():
    post = postform()
    message = None
    fmessage = None


    if post.validate_on_submit():
        try:
            con = get_db_connection()

            title = post.Title.data
            content = post.content.data
            image = post.image.data

            filename = image.filename
            image.save(f"static/img/course/{filename}")

            teacher = session["username"]

            con.execute(
                "INSERT INTO write(title, content, img, teacher) VALUES (?, ?, ?, ?)",
                (title, content, filename, teacher)
            )

            con.commit()
            message = 'Post published successfully!'
            flash(message, "success")
            return redirect(url_for("write"))


        except sqlite3.Error:
            fmessage = 'There is an error with the database.'
            flash(fmessage, "danger")

        finally:
            con.close()

    return render_template(
        "write.html",
        title="Teacher",
        post=post,
        message = message,
        fmessage = fmessage


    )




@app.route("/Profile")
def Profile():
    fname = session["fname"]
    lname =  session["lname"]
    user= session["username"]
    email = session["email"]
    

    return render_template("Profile.html", title="Profile", first=fname , last=lname, name=user, mail=email)

@app.route("/coursess")
def coursess():
    conn = get_db_connection()
    available_courses = conn.execute("SELECT Name, start_time ,end_time, icon FROM coursess").fetchall()
    conn.close()
    
    return render_template("coursess.html", title="coursess", courses=available_courses )

@app.route("/Today")
def Today():
    conn = get_db_connection()
    now = datetime.date.today()
    word = now.strftime("%A")
    available_courses = conn.execute(
    "SELECT * FROM coursess WHERE day = ?",
    (word,)
).fetchall()
    return render_template("Today.html", title="Today",today=word , courses=available_courses )


@app.route("/today/<day>")
def today(day):
    conn = get_db_connection()

    courses = conn.execute(
        "SELECT * FROM coursess WHERE day = ?",
        (day,)
    ).fetchall()

    conn.close()

    return render_template("coursess.html", courses=courses, day=day)




@app.route("/attendance")
def attendance():
    conn = get_db_connection() 
    token = session.get("qr_token")
    uname = session.get("username") 
    id = session.get("id")
    courses_status = []

    if not token or not uname:
        return "برجاء تسجيل الدخول أولاً", 401
  
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=20,
        border=8
    )
    # نضع داخل الـ QR رابط دالة فحص السكاّن (التي سنصنعها بالأسفل)
    qr.add_data(f"http://127.0.0.1:5000/attendance/{token}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="white")
    img.save(f"static/img/Qr code/{uname}.png")
    
    # 2. جلب تاريخ ووقت السيرفر الحالي
    now = datetime.datetime.now()
    current_day = now.strftime("%A")     # اسم اليوم (مثال: Thursday)
    current_time = now.strftime("%H:%M")        # الوقت الحالي (ساعة، دقيقة)


    courses = conn.execute(
        "SELECT * FROM coursess WHERE day = ?",
        (current_day,)
    ).fetchall()

    

    
    for course in courses:

        attendance = conn.execute("""
            SELECT *
            FROM attendance
            WHERE student_id = ?
            AND course_id = ?
        """, (id, course["id"])).fetchone()

        if current_time < course["start_time"]:
            status = "Upcoming"

        elif course["start_time"] <= current_time <= course["end_time"]:
            if attendance:
                status = "Attendance"
            else:
                status = "Going"

        else:
            if attendance:
                status = "Attendance"
            else:
                status = "Absent"

        courses_status.append({"course": course, "status": status})

    conn.close()
    

    # إرسال البيانات الجاهزة لصفحة الـ HTML
    return render_template("attendance.html", title="attendance", student=uname , courses=courses_status)


    
@app.route("/attendance/<token>")
def attendance_check(token):
    now = datetime.datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    conn = get_db_connection()

    # التحقق من الطالب
    student = conn.execute(
        "SELECT * FROM student WHERE qr_token = ?",
        (token,)
    ).fetchone()

    if not student:
        conn.close()
        return "Invalid QR"

    # جميع الكورسات الجارية الآن
    current_courses = conn.execute("""
        SELECT *
        FROM coursess
        WHERE day = ?
        AND start_time <= ?
        AND end_time >= ?
    """, (current_day, current_time, current_time)).fetchall()

    # لا يوجد كورس
    if len(current_courses) == 0:

        next_course = conn.execute("""
            SELECT *
            FROM coursess
            WHERE day = ?
            AND start_time > ?
            ORDER BY start_time
            LIMIT 1
        """, (current_day, current_time)).fetchone()

        conn.close()

        if next_course:
            return f"No course is running now.<br>Next course: {next_course['Name']} at {next_course['start_time']}"
        else:
            return "No course is scheduled today."

    # يوجد كورس واحد
    elif len(current_courses) == 1:

        current_course = current_courses[0]

        already = conn.execute("""
            SELECT *
            FROM attendance
            WHERE student_id = ?
            AND course_id = ?
            AND attendance_date = ?
        """, (
            student["id"],
            current_course["id"],
            today
        )).fetchone()

        if already:
            conn.close()
            return "Attendance already registered."

        conn.execute("""
            INSERT INTO attendance
            (student_id, course_id, status, attendance_date, attendance_time)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student["id"],
            current_course["id"],
            "Attendance",
            today,
            current_time
        ))

        conn.commit()
        conn.close()

        return f"Attendance registered for {current_course['Name']}"

    # يوجد أكثر من كورس
    else:
        conn.close()

        return render_template(
            "choose_course.html",
            token=token,
            courses=current_courses
        )


@app.route("/save_attendance", methods=["POST"])
def save_attendance():

    token = request.form["token"]
    course_id = request.form["course_id"]

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM student WHERE qr_token = ?",
        (token,)
    ).fetchone()

    if not student:
        conn.close()
        return "Invalid QR"

    already = conn.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
        AND course_id = ?
        AND attendance_date = ?
    """, (
        student["id"],
        course_id,
        today
    )).fetchone()

    if already:
        conn.close()
        return "Attendance already registered."

    conn.execute("""
        INSERT INTO attendance
        (student_id, course_id, status, attendance_date, attendance_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student["id"],
        course_id,
        "Attendance",
        today,
        current_time
    ))

    conn.commit()
    conn.close()

    return "Attendance registered successfully."
    
            
@app.route("/Dashboard")
def Dashboard():
    now = datetime.datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    Email = session.get('mail')
    user =session.get('username')

    conn = get_db_connection()

    next_course = conn.execute("""
        SELECT *
        FROM coursess
        WHERE day = ?
        AND start_time > ?
        ORDER BY start_time
        LIMIT 1
    """, (current_day, current_time)).fetchone()

    remaining_time = None
    hours = 0
    minutes = 0
    remaining = None


    if next_course:
        # وقت بداية الكورس
        start_time = datetime.datetime.strptime(
            next_course["start_time"], "%H:%M"
        ).replace(
            year=now.year,
            month=now.month,
            day=now.day
        )
        remaining = start_time - now
        total_seconds = int(remaining.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

    now = datetime.datetime.now()

    notification = None

   

    if next_course:

        start_time = datetime.datetime.strptime(
            next_course["start_time"], "%H:%M"
        ).replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

        remaining = start_time - now

        total_seconds = int(remaining.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if datetime.timedelta(minutes=0) < remaining <= datetime.timedelta(minutes=15):

            # Notification مرة واحدة
            if not session.get("notification_sent", False):

                notification = {
                    "title": "Course Reminder",
                    "message": f"{next_course['Name']} starts in {remaining.seconds // 60} minutes."
                }

                session["notification_sent"] = True

            # Email مرة واحدة
            if not session.get("email_sent", False):

                send_course_email(
                    receiver_email=Email,
                    student_name=user,
                    course_name=next_course["Name"],
                    day=next_course["day"],
                    time=next_course["start_time"]
                )

                session["email_sent"] = True

    # بعد انتهاء الحصة نسمح بإرسال التذكير للحصة التالية
    if remaining is not None and remaining <= datetime.timedelta(seconds=0):
        session["notification_sent"] = False
        session["email_sent"] = False





    user = session['username']
    return render_template("Dashboard.html",title="Dashboard",next_course=next_course,hours=f"{hours:02}",
    minutes=f"{minutes:02}" , notification=notification , user=user)




@app.route("/Teacher")
def Teacher ():
    return render_template("Teacher.html", title="Teacher")

@app.route("/preparation")
def preparation ():
    con = get_db_connection()

    posts = con.execute("SELECT  title, content, img, teacher FROM write ").fetchall()
    con.commit()
    con.close()

    print(posts)

    return render_template("preparation.html", title="preparation" , cpost=posts)



@app.before_request
def require_login():
    allowed_routes = [
        "load",
        "login",
        "register",
        "Main",
        "static",   # مهم جدًا
    ]

    if request.endpoint in allowed_routes:
        return

    if "username" not in session:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)


   