#REQUIREMENT
# - Client need to enter his/her email, DOB and last 4 digits of SSN/ITIN
# - If matches data on DB, then automatically send an email with unique URL of his/her questionnaire
# - If not, the error page appears and "trial_count" increases
# - The trial_count can be no more than 5. If it exceeds 5, the error page appears.

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app: Flask = Flask(__name__)

# Email system config
load_dotenv()
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL','').lower() in ['true', '1', 'yes']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Setting DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# DB Model
class UserData(db.Model):
    # Email is the primary key of this DB
    email = db.Column(db.String(100),primary_key=True)
    # 8 digits of Date Of Birth
    dob = db.Column(db.Integer)
    # last 4 digits of SSN or ITIN
    pw = db.Column(db.Integer)
    # Residency Status R or NR
    residency = db.Column(db.String(2))
    # Token for this client for security
    urltoken = db.Column(db.String(32))
    # The date when this system sent the unique URL to client
    sent_date = db.Column(db.DateTime)
    # How many times the client or other person tried to verify the emails etc
    trial_count = db.Column(db.Integer)
    # Name on the email i.e. Atena
    name_on_email = db.Column(db.String(100))

# Routing for when the client accesses the common URL
@app.route("/")
def webq_send():
    if request.method =='GET':
        return render_template("webq_send.html")

# Routing for when the client submitted the verification info
# Only POST method is allowed
@app.route("/webq_sent", methods=["POST"])
def webq_sent():
    if request.method == 'POST':
        # These are the data which client sends
        email: str = request.form.get("email")
        dob: int = request.form.get("dob")
        pw: int = request.form.get("pw")

        # Filtering user
        user = UserData.query.filter_by(email=email).first()
        if (int(user.dob) == int(dob) and int(user.pw) == int(pw) and int(user.trial_count) < 6):
            # Matched
            msg = Message(
                'This is your web questionnaire URL!',
                recipients = [email]
            )
            msg.body = 'Please see below:'+dob
            mail.send(msg)
            return render_template("webq_sent.html")
        else:
            # Not matched, then count up
            user.trial_count += 1
            db.session.commit()
            return render_template("error.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
