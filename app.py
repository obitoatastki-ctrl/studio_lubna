from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "studio_lobna_secret"

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# صفحة من نحن
@app.route("/about")
def about():
    return render_template("about.html")

# صفحة الخدمات
@app.route("/services")
def services():
    return render_template("services.html")

# صفحة طلب خدمة
@app.route("/request_service", methods=["GET", "POST"])
def request_service():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        service = request.form["service"]
        message = request.form["message"]

        msg = MIMEText(f"طلب خدمة جديد من {name}\nالبريد: {email}\nالخدمة المطلوبة: {service}\n\nالرسالة:\n{message}")
        msg["Subject"] = "🛎️ طلب خدمة جديد من موقع استوديو لبنة"
        msg["From"] = "lobnataib2@gmail.com"
        msg["To"] = "lobnataib2@gmail.com"

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("lobnataib2@gmail.com", "كلمة_مرور_التطبيق_الخاصة_بجيميل")
                server.send_message(msg)
            flash("✅ تم إرسال طلبك بنجاح! سنتواصل معك قريبًا.", "success")
        except Exception as e:
            print("Error:", e)
            flash("❌ حدث خطأ أثناء إرسال الطلب. حاول مجددًا.", "error")

        return redirect("/request_service")

    return render_template("request_service.html")

# صفحة الاتصال
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        msg = MIMEText(f"رسالة جديدة من {name}\nالبريد: {email}\n\n{message}")
        msg["Subject"] = "📩 رسالة جديدة من موقع استوديو لبنة"
        msg["From"] = "lobnataib2@gmail.com"
        msg["To"] = "lobnataib2@gmail.com"

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("lobnataib2@gmail.com", "كلمة_مرور_التطبيق_الخاصة_بجيميل")
                server.send_message(msg)
            flash("✅ تم إرسال رسالتك بنجاح!", "success")
        except Exception as e:
            print("Error:", e)
            flash("❌ حدث خطأ أثناء إرسال الرسالة.", "error")

        return redirect("/contact")

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
