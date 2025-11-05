from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"  # لتأمين الجلسات والرسائل

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_name = request.form["name"]
        user_email = request.form["email"]
        user_message = request.form["message"]

        msg = EmailMessage()
        msg["Subject"] = "📩 رسالة جديدة من موقع Studio Lobna"
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = os.getenv("EMAIL_RECEIVER", "lobnataib2@gmail.com")
        msg.set_content(
            f"المرسل: {user_name}\nالبريد: {user_email}\n\nالرسالة:\n{user_message}"
        )

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                server.send_message(msg)
            flash("✅ تم إرسال رسالتك بنجاح! شكراً لتواصلك معنا ❤️", "success")
        except Exception as e:
            print("Error:", e)
            flash("❌ حدث خطأ أثناء إرسال الرسالة. حاول لاحقاً.", "error")

        return redirect("/contact")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
