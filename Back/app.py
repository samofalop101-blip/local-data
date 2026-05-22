from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------------
# LOAD ENV VARIABLES
# -------------------------
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

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

    name   = data.get("name",   "").strip()
    email  = data.get("email",  "").strip()
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
    # EMAIL 1 — NOTIFY YOU
    # Sends registration details to YOUR inbox
    # -------------------------
    admin_subject = f"New Registration — {name}"
    admin_body    = f"""
New student registration received.

Name:    {name}
Email:   {email}
Course:  {course}

Please follow up with this student.
"""

    admin_msg            = MIMEText(admin_body)
    admin_msg["Subject"] = admin_subject
    admin_msg["From"]    = EMAIL_USER
    admin_msg["To"]      = EMAIL_TO        # ← goes to YOUR inbox

    # -------------------------
    # EMAIL 2 — CONFIRM TO STUDENT
    # Sends confirmation to the STUDENT
    # -------------------------
    student_subject = f"Registration Successful — {course}"
    student_body    = f"""
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

    student_msg            = MIMEText(student_body)
    student_msg["Subject"] = student_subject
    student_msg["From"]    = EMAIL_USER
    student_msg["To"]      = email         # ← goes to STUDENT inbox

    # -------------------------
    # SEND BOTH EMAILS
    # -------------------------
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        server.send_message(admin_msg)     # notify you
        server.send_message(student_msg)   # confirm to student

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