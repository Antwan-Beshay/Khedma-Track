import smtplib
from email.mime.text import MIMEText
from email.header import Header

# بيانات الحساب
sender_email = "antwanbeshay260@gmail.com"
app_password = "sgan xoca eogb bqdo"   # ضع App Password الخاص بك هنا
receiver_email = "antwanhany260@gmail.com"

# بيانات الطالب والحصة
student_name = "Ant"
course_name = "Programming"
day = "Sunday"
time = "9:00 AM"

subject = "Reminder: Your class starts in 15 minutes"

body = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">

<style>
body{{
    font-family:Arial,sans-serif;
    background:#f5f5f5;
    margin:0;
    padding:30px;
}}

.container{{
    max-width:600px;
    margin:auto;
    background:#fff;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 5px 15px rgba(0,0,0,.1);
}}

.header{{
    background:#0d6efd;
    color:#fff;
    text-align:center;
    padding:25px;
}}

.content{{
    padding:30px;
    color:#333;
    line-height:1.8;
}}

.course{{
    background:#eef5ff;
    border-right:5px solid #0d6efd;
    padding:15px;
    border-radius:8px;
    margin:20px 0;
}}

.btn{{
    display:inline-block;
    background:#0d6efd;
    color:#fff !important;
    text-decoration:none;
    padding:12px 24px;
    border-radius:8px;
    font-weight:bold;
}}

.footer{{
    text-align:center;
    color:#888;
    padding:20px;
    font-size:14px;
}}
</style>

</head>

<body>

<div class="container">

    <div class="header">
        <h2>📚 تذكير بموعد الحصة</h2>
    </div>

    <div class="content">

        <p>مرحبًا <strong>Antwan</strong>،</p>

        <p>
            نذكرك بأن حصتك ستبدأ بعد
            <strong>15 دقيقة</strong>.
        </p>

        <div class="course">
            <p><strong>📖 المادة:</strong> COMPUTER</p>
            <p><strong>📅 اليوم:</strong> SUNDAY</p>
            <p><strong>🕒 الوقت:</strong> 9</p>
        </div>

        <div style="text-align:center;margin:30px 0;">
            <a href="http://127.0.0.1:5000/login" class="btn">
                فتح النظام
            </a>
        </div>

        <p>
            نتمنى لك حصة ممتعة ومثمرة 🌟
        </p>

    </div>

    <div class="footer">
        Service Preparation Learning System
    </div>

</div>

</body>
</html>
"""

# إنشاء الرسالة
msg = MIMEText(body, "html", "utf-8")
msg["Subject"] = Header(subject, "utf-8")
msg["From"] = sender_email
msg["To"] = receiver_email

# إرسال البريد
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("✅ Email sent successfully!")

except Exception as e:
    print("❌ Failed to send email:")
    print(e)