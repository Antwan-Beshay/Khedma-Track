import qrcode
from qrcode.constants import ERROR_CORRECT_H

qr = qrcode.QRCode(
    version=None,
    error_correction=ERROR_CORRECT_H,
    box_size=20,
    border=8
)

# البيانات التي ستوضع داخل الـ QR
qr.add_data("https://mysite.com")

# إنشاء الـ QR
qr.make(fit=True)

# إنشاء الصورة
img = qr.make_image(
    fill_color="#000000",
    back_color="white"
)

# حفظ الصورة
img.save("static/img/Qr code/qr_logo.png")