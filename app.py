from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# قائمة الكلمات الممنوعة
bad_words = ["شتم1", "شتم2", "شتم3"]  # ضع الكلمات التي تريد فلترتها هنا

def filter_bad_comments(comment):
    for word in bad_words:
        if word.lower() in comment.lower():
            return "تم حظر تعليقك لاحتوائه على كلمات غير لائقة."
    return comment

def send_notification(name, email, service):
    msg = MIMEText(f"تم استلام طلب خدمة جديد من {name}.\nالبريد: {email}\nالخدمة: {service}")
    msg['Subject'] = "طلب خدمة جديد"
    msg['From'] = "tb-loubna44@gmail.com"
    msg['To'] = "tb-loubna44@gmail.com"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tb-loubna44@gmail.com", "كلمة_المرور_هنا")  # ضع كلمة المرور الصحيحة
    server.send_message(msg)
    server.quit()

def send_auto_reply(user_email, user_name):
    msg = MIMEText(f"مرحباً {user_name},\nشكراً لتواصلك معنا! سنقوم بالرد عليك في أقرب وقت.")
    msg['Subject'] = "تم استلام طلبك"
    msg['From'] = "tb-loubna44@gmail.com"
    msg['To'] = user_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tb-loubna44@gmail.com", "كلمة_المرور_هنا")  # ضع كلمة المرور الصحيحة
    server.send_message(msg)
    server.quit()

# الصفحة الرئيسية
@app.route('/')
@app.route('/<lang>/')
def index(lang='ar'):
    return render_template(f'{lang}/index.html')

# صفحة الأعمال
@app.route('/<lang>/works')
def works(lang='ar'):
    return render_template(f'{lang}/works.html')

# صفحة طلب الخدمة
@app.route('/<lang>/request_service', methods=['GET','POST'])
def request_service(lang='ar'):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        service = request.form['service']
        send_notification(name, email, service)
        send_auto_reply(email, name)
        return f"تم استلام طلبك {name}. شكراً لتواصلك!"
    return render_template(f'{lang}/request_service.html')

# صفحة الدفع
@app.route('/<lang>/pay', methods=['GET','POST'])
def pay(lang='ar'):
    if request.method == 'POST':
        method = request.form['payment_method']
        return f"تم اختيار الدفع عبر: {method}. سيتم تفعيل الخدمة بعد الدفع."
    return render_template(f'{lang}/pay.html')

# مثال لتسجيل التعليقات (فلترة)
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    comment = request.form['comment']
    filtered = filter_bad_comments(comment)
    # هنا يمكن حفظ التعليق في قاعدة بيانات أو ملف
    return f"تعليقك: {filtered}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
