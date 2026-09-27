from email.mime import message
import traceback
from flask import Flask, flash, redirect , render_template , url_for , session , request
import sqlite3
import datetime
import secrets
from form import registerForm ,loginform
from Forget import forgotPasswordForm, codeForm, resetPasswordForm
from secret import SecretKeyForm
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from upload import postform
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "secret.env"))
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(Exception)
def handle_exception(error):
    traceback.print_exc()
    return render_template("500.html"), 500

def send_course_email(receiver_email, student_name, course_name, day, time):

    sender_email = os.getenv("MAIL_USERNAME")

    app_password = os.getenv("MAIL_PASSWORD")

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


def codeemail(receiver_email,  verification_code):

    sender_email = os.getenv("MAIL_USERNAME")

    app_password = os.getenv("MAIL_PASSWORD")

    subject = "Your Verification Code"

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body style="
        margin:0;
        padding:40px 0;
        background:#eef4ff;
        font-family:Arial, Helvetica, sans-serif;
    ">

        <div style="
            width:90%;
            max-width:450px;
            margin:auto;
            background:#ffffff;
            padding:40px 25px;
            text-align:center;
            border-radius:25px;
            box-shadow:0 20px 50px rgba(30,58,95,0.18);
        ">

            <!-- استبدال الأيقونة بكود SVG متوافق مع كافة برامج الإيميل -->
            <div style="
                width:80px;
                height:80px;
                margin:auto;
                border-radius:50%;
                background:#eef4ff;
                border:2px solid #1E3A5F;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-key" viewBox="0 0 16 16">
  <path d="M0 8a4 4 0 0 1 7.465-2H14a.5.5 0 0 1 .354.146l1.5 1.5a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0L13 9.207l-.646.647a.5.5 0 0 1-.708 0L11 9.207l-.646.647a.5.5 0 0 1-.708 0L9 9.207l-.646.647A.5.5 0 0 1 8 10h-.535A4 4 0 0 1 0 8m4-3a3 3 0 1 0 2.712 4.285A.5.5 0 0 1 7.163 9h.63l.853-.854a.5.5 0 0 1 .708 0l.646.647.646-.647a.5.5 0 0 1 .708 0l.646.647.646-.647a.5.5 0 0 1 .708 0l.646.647.793-.793-1-1h-6.63a.5.5 0 0 1-.451-.285A3 3 0 0 0 4 5"/>
  <path d="M4 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
</svg>
            </div>

            <h2 style="
                color:#1E3A5F;
                margin-top:25px;
            ">
                Your Verification Code
            </h2>

            <p style="
                color:#24324a;
                font-size:16px;
                line-height:1.7;
            ">
                We received a request to reset your password.
            </p>

            <p style="
                color:#24324a;
                font-size:16px;
            ">
                Your verification code is:
            </p>

            <div style="
                margin:25px auto;
                padding:18px;
                width:180px;
                background:#eef4ff;
                border:2px solid #1E3A5F;
                border-radius:15px;
                color:#1E3A5F;
                font-size:32px;
                font-weight:bold;
                letter-spacing:8px;
            ">
                {verification_code}
            </div>

            <p style="
                color:#667085;
                font-size:14px;
                line-height:1.6;
            ">
                Enter this code on the SPS password reset page.
            </p>

            <p style="
                color:#667085;
                font-size:13px;
            ">
                If you did not request this code, you can safely ignore
                this email.
            </p>

            <hr style="
                border:0;
                border-top:1px solid #eeeeee;
                margin:30px 0;
            ">

            <p style="
                color:#667085;
                font-size:13px;
            ">
                SPS - Service Preparation System
            </p>

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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
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
        user = conn.execute('SELECT * FROM student WHERE  email= ?', 
                            (mail,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["email_sent"] = False
            session["notification_sent"] = False
            session['id'] = user['id']
            session['mail'] = user['email']
            session['role'] = user['role']
            session['fname'] = user['fname']
            session['lname'] = user['lname']
            session["username"] = user['uname']
            session["qr_token"] = user['qr_token']
            next_url = session.pop("next_url", None)
            if next_url:
                return redirect(next_url)
            role = session['role']
            if role == "student" or  role == "Student" :
                return redirect(url_for("Dashboard"))
            else:
                return redirect(url_for("Secret_Key"))
                
        else:
            fmesage = "email or password is not correct."
            flash(fmesage, "danger")

    return render_template("login.html", title="Login", form=form ,message= fmesage )
    

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = forgotPasswordForm()
    message = None
    if form.validate_on_submit():
        email = form.email.data
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM student WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user:
            reset_code = str(secrets.randbelow(1000000)).zfill(6)
            session["reset_code"] = reset_code
            session["reset_email"] = email

            try:
                codeemail(receiver_email=email, verification_code=reset_code)
                message2 = "A reset code has been sent to your email."
                flash(message2, "success")
                return redirect(url_for("code"))
            except Exception as e:
                message = f"Failed to send email: {e}"
                flash(message, "danger")
        else:
            message = "No account found with that email."
            flash(message, "danger")

   

    return render_template(
        "forgot_password.html",
        title="Forgot Password",
        form=form,
        message=message
    )

@app.route("/code", methods=["GET", "POST"])
def code():
    message = None
    form = codeForm()

    if form.validate_on_submit():
        entered_code = form.code.data
        reset_code = session.get("reset_code")

        if entered_code == reset_code:
            session["code_verified"] = True
            flash("Code verified. You can now reset your password.", "success")
            return redirect(url_for("reset_password"))

        message = "Invalid code. Please try again."

    return render_template(
        "code.html",
        title="Enter Code",
        form=form,
        message=message
    )
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    message = None
    form = resetPasswordForm()

    if not session.get("code_verified"):
        message = "You must verify the code before resetting your password."
        flash(message, "danger")
        return redirect(url_for("forgot_password"))

    if form.validate_on_submit():
        new_password = form.password.data
        email = session.get("reset_email")

        if not email:
            message = "Your session has expired. Please request a new code."
            flash(message, "danger")
        elif new_password != form.confirm_password.data:
            message = "Passwords do not match."
            flash(message, "danger")
        else:
            hashed_password = generate_password_hash(new_password)

            conn = get_db_connection()
            conn.execute(
                "UPDATE student SET password = ? WHERE email = ?",
                (hashed_password, email)
            )
            conn.commit()
            conn.close()

            session.pop("reset_code", None)
            session.pop("reset_email", None)
            session.pop("code_verified", None)      

            flash("Your password has been reset successfully.", "success")

            if session.get("role") in ["student", "Student"]:
                return redirect(url_for("Dashboard"))
            else:
                return redirect(url_for("Secret_Key"))

    return render_template(
        "Newpass.html",
        title="Reset Password",
        form=form,
        message=message
    )
@app.route("/register", methods=["GET", "POST"])
def register():
    token = secrets.token_urlsafe(32)
    form = registerForm()  
    fmessage = None
    
    if form.validate_on_submit():
        flash("Account created for {}!".format(form.uname.data), "success")
    
        try:
            hashed_password = generate_password_hash(form.password.data)
            conect = sqlite3.connect(DATABASE)
            cursor = conect.cursor()
            cursor.execute("insert into student (fname ,  lname , uname ,email, password, role , qr_token) Values(?, ?, ?, ?, ?, ?, ?)",(form.fname.data ,form.lname.data, form.uname.data ,form.email.data , hashed_password, form.role.data,token))
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
                return redirect(url_for("Secret_Key"))
        except sqlite3.IntegrityError :
            fmessage = 'Username or email already exists'
            flash(fmessage, "danger")
        finally:
            conect.close()
    if form.is_submitted() and not form.validate():
        fmessage = 'Please correct the errors in the form.'
        flash(fmessage, "danger")
    return render_template("register.html", title="Register", form=form , message= fmessage)

@app.route("/Secret_Key" , methods=["GET", "POST"])
def Secret_Key():
    
    if session.get("role") not in ["teacher", "Teacher"]:
        flash("You do not have permission to access this page.", "danger")
        return render_template("403.html"), 403
    message = ""
    secret_form = SecretKeyForm()
    secret = "s7hW6mKDK3dANg"
    ssecret = "nBRFQBzTHrGlGg"
    data = secret_form.Secret_Key.data
    if secret_form.validate_on_submit():
        if data == secret:
            flash("Secret Key is correct.", "success")
            return redirect(url_for("write"))
        elif data == ssecret:
            session['role']= "Admin"
            flash("Secret Key is correct.", "success")
            return redirect(url_for("admin"))
        else:
            message = "Incorrect Secret Key. Please try again."
            flash(message, "danger")

    return render_template("upload.html", title="Secret_Key",secret_form=secret_form, message=message)
    



@app.route("/admin")
def admin():
    if session.get("role") not in ["admin", "Admin"]:
        flash("You do not have permission to access this page.", "danger")
        return render_template("403.html"), 403

    con = get_db_connection()

    students = con.execute("""
        SELECT *
        FROM student
    """).fetchall()



    Teachers = con.execute("""
        SELECT *
        FROM student
        WHERE role = ?
    """, ("teacher",)).fetchall()


    Tcount= con.execute("""
            SELECT COUNT(*) AS count
            FROM student where role = "teacher"
        """).fetchone()["count"]
    
    Scount= con.execute("""
                SELECT COUNT(*) AS count
                FROM student where role = "student"
            """).fetchone()["count"]


    total = con.execute("""
            SELECT COUNT(*) AS count
            FROM student 
        """).fetchone()["count"]
    con.close()

    return render_template(
        "admin.html",
        title="Admin",
        students=students,
        Teachers=Teachers,
        cstudent= Scount , 
        cTeacher =  Tcount,   
        total= total
    )

@app.route("/write", methods=["GET", "POST"])
def write():
    if session.get("role") not in ["teacher", "Teacher"]:
        flash("You do not have permission to access this page.", "danger")
        return render_template("403.html"), 403
    
    post = postform()
    message = None
    print(message)

    if post.validate_on_submit():
        print(f"message:{message}")
        try:
            print(message)
            con = get_db_connection()

            title = post.Title.data
            content = post.content.data
            image = post.image.data
            filename = image.filename
            print(f"message:{message}2")

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
            message = 'There is an error with the database.'
            flash(message, "danger")

        finally:
            con.close()

    return render_template(
        "write.html",
        title="Teacher",
        post=post,
        message = message,
    )


@app.route("/Awrite", methods=["GET", "POST"])
def Awrite():
    if session.get("role") not in ["Admin", "admin"]:
        flash("You do not have permission to access this page.", "danger")
        return render_template("403.html"), 403
    
    post = postform()
    message = None
    print(message)

    if post.validate_on_submit():
        print(f"message:{message}")
        try:
            print(message)
            con = get_db_connection()

            title = post.Title.data
            content = post.content.data
            image = post.image.data
            filename = image.filename
            print(f"message:{message}2")

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
            return redirect(url_for("Awrite"))


        except sqlite3.Error:
            message = 'There is an error with the database.'
            flash(message, "danger")

        finally:
            con.close()

    return render_template(
        "Awrite.html",
        title="Admin - post",
        post=post,
        message = message,
    )




@app.route("/Profile")
def Profile():
    if session.get("role") not in ["student", "Student"]:
                flash("You do not have permission to access this page.", "danger")
                return render_template("403.html"), 403
    fname = session["fname"]
    lname =  session["lname"]
    user= session["username"]
    email = session.get('mail') or session.get('email')
    

    return render_template("Profile.html", title="Profile", first=fname , last=lname, name=user, mail=email)


@app.route("/TProfile")
def TProfile():
    if session.get("role") not in ["teacher", "Teacher"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
    fname = session.get("fname")
    lname = session.get("lname")
    user = session.get("username")
    email = session.get("mail") or session.get("email")
    role = session.get("role")

    return render_template("Tprofile.html", title="Teacher Profile", first=fname , last=lname, name=user, mail=email, role=role)


@app.route("/AProfile")
def AProfile():
    if session.get("role") not in ["Admin", "admin"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
    fname = session.get("fname")
    lname = session.get("lname")
    user = session.get("username")
    email = session.get("mail") or session.get("email")
    role = session.get("role")

    return render_template("Aprofile.html", title="Admin- Profile", first=fname , last=lname, name=user, mail=email, role=role)

@app.route("/coursess")
def coursess():
    if session.get("role") not in ["student", "Student"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
    conn = get_db_connection()
    available_courses = conn.execute("SELECT Name, start_time ,end_time, icon FROM coursess").fetchall()
    conn.close()
    
    return render_template("coursess.html", title="coursess", courses=available_courses )

@app.route("/Today")
def Today():
    if session.get("role") not in ["student", "Student"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
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
    if session.get("role") not in ["student", "Student"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
    conn = get_db_connection()

    courses = conn.execute(
        "SELECT * FROM coursess WHERE day = ?",
        (day,)
    ).fetchall()

    conn.close()

    return render_template("coursess.html", courses=courses, day=day)

def attande():
    now = datetime.datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    conn = get_db_connection()

    try:
        courses = conn.execute("""
            SELECT *
            FROM coursess
            WHERE day = ?
            AND end_time <= ?
        """, (current_day, current_time)).fetchall()

        students = conn.execute("""
            SELECT id
            FROM student
            WHERE role = 'student' OR role = 'Student'
        """).fetchall()

        for course in courses:
            for student in students:

                student_id = student["id"]

                attendance = conn.execute("""
                    SELECT *
                    FROM attendance
                    WHERE student_id = ?
                    AND course_id = ?
                    AND attendance_date = ?
                """, (
                    student_id,
                    course["id"],
                    today
                )).fetchone()

                if current_time < course["start_time"]:
                    status = "Upcoming"

                elif course["start_time"] <= current_time <= course["end_time"]:
                    if attendance:
                        status = attendance["status"]
                    else:
                        status = "Going"

                else:
                    if attendance:
                        status = attendance["status"]
                    else:
                        conn.execute("""
                            INSERT INTO attendance
                            (student_id, course_id, status, attendance_date, attendance_time)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            student_id,
                            course["id"],
                            "Absent",
                            today,
                            current_time
                        ))

                        conn.commit()

                        status = "Absent"

        conn.commit()

    except Exception as e:
        print("Attendance Scheduler Error:", e)

    finally:
        conn.close()
    


@app.route("/attendance")
def attendance():
    if session.get("role") not in ["student", "Student"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
    now = datetime.datetime.now()
    current_day = now.strftime("%A")     
    current_time = now.strftime("%H:%M")        
    today = now.strftime("%Y-%m-%d")
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
    qr.add_data(f"{request.host_url}attendance/{token}")

    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="white")
    img.save(f"static/img/Qr code/{uname}.png")
    
   
  


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
            AND attendance_date = ?
        """, (id, course["id"], today)).fetchone()   

        if current_time < course["start_time"]:
            status = "Upcoming"

        elif course["start_time"] <= current_time <= course["end_time"]:
            if attendance:
                status = attendance["status"]
            else:
                status = "Going"

        else:
            if attendance:
                status = attendance["status"]
            else:
                conn.execute("""
                            INSERT INTO attendance
                            (student_id, course_id, status, attendance_date, attendance_time)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            id,
                            course["id"],
                            "Absent",
                            today,
                            current_time
                        ))
                
                conn.commit()
    

                status = "Absent"

        courses_status.append({"course": course, "status": status})

    conn.close()
    

    return render_template("attendance.html", title="attendance", student=uname , courses=courses_status)


    
@app.route("/attendance/<token>")
def attendance_check(token):
    now = datetime.datetime.now()
    current_day = now.strftime("%A")
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

    current_courses = conn.execute("""
        SELECT *
        FROM coursess
        WHERE day = ?
        AND start_time <= ?
        AND end_time >= ?
    """, (current_day, current_time, current_time)).fetchall()

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

    else:
        current_course_ids = [course["id"] for course in current_courses]

        placeholders = ",".join(["?"] * len(current_course_ids))

        already = conn.execute(f"""
            SELECT attendance.*, coursess.Name
            FROM attendance
            JOIN coursess ON attendance.course_id = coursess.id
            WHERE attendance.student_id = ?
            AND attendance.attendance_date = ?
            AND attendance.course_id IN ({placeholders})
        """, (student["id"], today, *current_course_ids)).fetchone()

        if already:
            conn.close()
            return f"You are already registered in {already['Name']}."
            

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
    

def check_and_send_reminders():
    conn = get_db_connection()
    try:
        now = datetime.datetime.now()
        current_day = now.strftime("%A")
        today_str = now.strftime("%Y-%m-%d")

        upcoming_courses = conn.execute("""
            SELECT * FROM coursess
            WHERE day = ? AND start_time > ?
        """, (current_day, now.strftime("%H:%M"))).fetchall()

        students = conn.execute("""
            SELECT id, uname, email
            FROM student
            WHERE role = 'student' OR role = 'Student'
        """).fetchall()

        for course in upcoming_courses:
            start_time = datetime.datetime.strptime(
                course["start_time"], "%H:%M"
            ).replace(year=now.year, month=now.month, day=now.day)
            remaining = start_time - now

            if datetime.timedelta(0) < remaining <= datetime.timedelta(minutes=15):
                for student in students:
                    already_sent = conn.execute("""
                        SELECT 1 FROM sent_notifications
                        WHERE course_id = ? AND student_id = ? AND notify_date = ?
                    """, (course["id"], student["id"], today_str)).fetchone()

                    if already_sent:
                        continue

                    try:
                        send_course_email(
                            receiver_email=student["email"],
                            student_name=student["uname"],
                            course_name=course["Name"],
                            day=course["day"],
                            time=course["start_time"]
                        )
                        conn.execute("""
                            INSERT INTO sent_notifications (course_id, student_id, notify_date)
                            VALUES (?, ?, ?)
                        """, (course["id"], student["id"], today_str))
                        conn.commit()
                    except Exception as e:
                        print(f"[reminder-error] student {student['id']}: {e}")
    finally:
        conn.close()

@app.route("/Dashboard")
def Dashboard():
    if session.get("role") not in ["student", "Student"]:
        flash("You do not have permission to access this page.", "danger")
        return render_template("403.html"), 403

    now = datetime.datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    today_str = now.strftime("%Y-%m-%d")
    Email = session.get('mail') or session.get('email')
    user = session.get('username')

    conn = get_db_connection()

    next_course = conn.execute("""
        SELECT *
        FROM coursess
        WHERE day = ?
        AND start_time > ?
        ORDER BY start_time
        LIMIT 1
    """, (current_day, current_time)).fetchone()

    remaining_seconds = None
    hours = 0
    minutes = 0
    remaining = None

    if next_course:
        start_time = datetime.datetime.strptime(
            next_course["start_time"], "%H:%M"
        ).replace(year=now.year, month=now.month, day=now.day)
        remaining = start_time - now
        remaining_seconds = int(remaining.total_seconds())

        total_seconds = remaining_seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if datetime.timedelta(minutes=0) < remaining <= datetime.timedelta(minutes=15):

            already_key = f"notified_{next_course['id']}_{today_str}"

            if not session.get(already_key, False):
                session["active_notification"] = {
                    "title": "Course Reminder",
                    "message": f"{next_course['Name']} starts in {remaining.seconds // 60} minutes.",
                    "course_id": next_course["id"],
                    "date": today_str
                }
                session[already_key] = True

            if not session.get("email_sent", False):
                try:
                    send_course_email(
                        receiver_email=Email,
                        student_name=user,
                        course_name=next_course["Name"],
                        day=next_course["day"],
                        time=next_course["start_time"]
                    )
                except Exception as e:
                    print(f"[dashboard-email-error] {e}")
                session["email_sent"] = True

    notification = session.get("active_notification")

    present = conn.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ? AND status = 'Attendance'
    """, (session["id"],)).fetchone()[0]

    absent = conn.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ? AND status = 'Absent'
    """, (session["id"],)).fetchone()[0]

    conn.close()

    total = present + absent
    attendance_rate = round((present / total) * 100) if total else 0

    if remaining is None or remaining <= datetime.timedelta(seconds=0):
        session["email_sent"] = False

    return render_template(
        "Dashboard.html", title="Dashboard", next_course=next_course,
        hours=f"{hours:02}", minutes=f"{minutes:02}",
        notification=notification, user=user,
        remaining_seconds=remaining_seconds, present=present,
        absent=absent, attendance_rate=attendance_rate
    )


@app.route("/Teacher")
def Teacher ():
    if session.get("role") not in ["teacher", "Teacher"]:
        flash("You do not have permission to access this page.", "danger")
        return render_template("403.html"), 403
    return render_template("Teacher.html", title="Teacher")

@app.route("/preparation")
def preparation ():
    if session.get("role") not in ["student", "Student"]:
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403
    con = get_db_connection()

    posts = con.execute("SELECT  title, content, img, teacher FROM write ").fetchall()
    con.commit()
    con.close()

    print(posts)

    return render_template("preparation.html", title="preparation" , cpost=posts)



@app.route("/logout")
def logout():
    session.clear()
    message = "You are loging out "
    flash(message, "info")
    return redirect(url_for("login"))


@app.route("/delete", methods=["POST"])
def delete():
    student_id = session.get("id")

    if not student_id:
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute(
            "DELETE FROM attendance WHERE student_id = ?",
            (student_id,)
        )

    conn.execute(
            "DELETE FROM sent_notifications WHERE student_id = ?",
            (student_id,)
        )

    conn.execute(
            "DELETE FROM student WHERE id = ?",
            (student_id,)
        )




    conn.commit()
    conn.close()

    session.clear()

    return redirect(url_for("login"))

@app.before_request
def require_login():
    allowed_routes = [
        "load",
        "login",
        "register",
        "Main",
        "static",
        "forgot_password",
        "code",
        "reset_password",
        "delete",

    ]

    if request.endpoint in allowed_routes:
        return

    if "username" not in session:
        session["next_url"] = request.url
        return redirect(url_for("login"))



scheduler = BackgroundScheduler()

scheduler.add_job(
    attande,
    'interval',
    minutes=1,
    id='attendance_job',
    replace_existing=True
)

scheduler.add_job(
    check_and_send_reminders,
    'interval',
    minutes=1,
    id='reminder_job',
    replace_existing=True
)

scheduler.start()

if __name__ == '__main__':
    app.run(
        debug=True,
        use_debugger=False,
        use_reloader=False
    )
