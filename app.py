
from flask import Flask, render_template, request
from database import init_db, save_analysis, get_history,save_contact
import re


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("submit.html")


 
@app.route("/analyze", methods=["POST"])
def analyze():

    job_title = request.form.get("job_title", "").strip()
    company_name = request.form.get("company_name", "").strip()
    job_text = request.form.get("job_text", "").strip()
    if len(job_title) > 150:
        return "Job title is too long.", 400

    if len(company_name) > 150:
        return "Company name is too long.", 400

    if not job_title or not company_name or not job_text:
        return "Please fill in all fields.", 400

    if len(job_text) > 5000:
        return "Advertisement is too long.", 400

    text = job_text.lower()

    warnings = []
    score = 0

    if "registration fee" in text:
        warnings.append("Registration fee requested")
        score += 40

    if "advance payment" in text:
        warnings.append("Advance payment requested")
        score += 40

    if "security deposit" in text:
        warnings.append("Security deposit requested")
        score += 30

    if "guaranteed job" in text:
        warnings.append("Guaranteed job claim")
        score += 15

    if "no interview" in text:
        warnings.append("No interview required")
        score += 15
    # Suspicious URL Detection

    suspicious_links = ["bit.ly", "tinyurl.com", "t.co"]
    for link in suspicious_links:
        if link in text:
            warnings.append("Suspicious shortened URL detected: " + link)
            score += 20
     # Suspicious Contact Detection

    if "gmail.com" in text:
        warnings.append("Personal Gmail address detected")
        score += 10

    if "yahoo.com" in text:
        warnings.append("Personal Yahoo email detected")
        score += 10
        # Phone Number Detection

    import re

    phone_pattern = r'\b(?:\+92|0)?3\d{9}\b'

    if re.search(phone_pattern, text):
        warnings.append("Mobile phone number detected")
        score += 10       
    score = min(score, 100)

    if score >= 60:
        risk = "High Risk"
    elif score >= 30:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    save_analysis(
        job_title,
        company_name,
        job_text,
        score,
        risk,
        warnings
    )
    
    return render_template(
        "result.html",
        job_title=job_title,
        company_name=company_name,
        result=risk,
        score=score,
        warnings=warnings
    )

@app.route("/history")
def history():

    records = get_history()

    return render_template(
        "history.html",
        records=records
    )
@app.route("/safety-tips")
def safety_tips():
    return render_template("safety_tips.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            return "Please fill in all fields.", 400
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Please enter a valid email address.", 400

        if len(name) > 100 or len(email) > 254 or len(message) > 2000:
            return "Input is too long.", 400

        save_contact(name, email, message)

        return render_template("contact_success.html") 
    return render_template("contact.html")
@app.route("/faq")
def faq():
    return render_template("faq.html")
@app.route("/dashboard")
def dashboard():
    records = get_history()

    total = len(records)

    high = sum(1 for r in records if r["risk_level"] == "High Risk")
    medium = sum(1 for r in records if r["risk_level"] == "Medium Risk")
    low = sum(1 for r in records if r["risk_level"] == "Low Risk")

    return render_template(
        "dashboard.html",
        total=total,
        high=high,
        medium=medium,
        low=low
    )


if __name__ == "__main__":

    init_db()

    app.run(host="127.0.0.1", port=5000, debug=True)