from flask import Flask, request, jsonify
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
app = Flask(__name__)
CORS(app)

# -------------------------
# API ROUTE
# -------------------------
@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    # -------------------------
    # VALIDATION
    # -------------------------
    if not name or not email or not course:
        return jsonify({
            "message": "All fields are required."
        }), 400

    # -------------------------
    # EMAIL CONTENT
    # -------------------------
    subject = "Registration Successful"

    body = f"""
Hello {name},

You have successfully registered for: {course}

Thank you for registering.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = email

    # -------------------------
    # SEND EMAIL VIA GMAIL SMTP
    # -------------------------
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return jsonify({
            "message": "Registration successful! Email sent."
        })

    except Exception as e:
        print("EMAIL ERROR:", e)

        return jsonify({
            "message": "Saved but email failed."
        }), 500

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)