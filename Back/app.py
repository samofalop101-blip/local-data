from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

import os
import smtplib
from email.mime.text import MIMEText

# -------------------------
# LOAD ENV VARIABLES
# -------------------------
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# -------------------------
# INIT FLASK APP
# -------------------------
app = Flask(__name__, static_folder=".")
CORS(app)

# -------------------------
# SERVE FRONTEND FILES
# -------------------------
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

# -------------------------
# API ROUTE
# -------------------------
@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid request. No data received."
        }), 400

    name   = data.get("name", "").strip()
    email  = data.get("email", "").strip()
    course = data.get("course", "").strip()

    # -------------------------
    # VALIDATION
    # -------------------------
    if not name:
        return jsonify({"message": "Please enter your name."}), 400

    if not email:
        return jsonify({"message": "Please enter your email."}), 400

    if not course:
        return jsonify({"message": "Please enter your course."}), 400

    # -------------------------
    # EMAIL CONTENT
    # -------------------------
    subject = f"Registration Successful — {course}"

    body = f"""
Hello {name},

You have successfully registered for: {course}

Here are your registration details:

  Name:    {name}
  Email:   {email}
  Course:  {course}

Thank you for registering. We will be in touch shortly.

---
This is an automated confirmation email.
"""

    msg             = MIMEText(body)
    msg["Subject"]  = subject
    msg["From"]     = EMAIL_USER
    msg["To"]       = email

    # -------------------------
    # SEND EMAIL VIA GMAIL SMTP
    # -------------------------
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print(f"[SUBMIT] ✅ Sent — {name} | {email} | {course}")

        return jsonify({
            "message": "Registration successful! A confirmation email has been sent."
        })

    except Exception as e:
        print(f"[SUBMIT] ❌ Email error: {e}")

        return jsonify({
            "message": "Registered but email could not be sent. Please contact us directly."
        }), 500

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )