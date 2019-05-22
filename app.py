from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from helper import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = """postgres://gbhqpfncjudmea:
9b9c6a51048fea29506932818111d9ad1132cb363e4f8416d639b4017ec36aac@
ec2-54-221-212-126.compute-1.amazonaws.com:5432/d1od71r3n81v0o?sslmode=require"""
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success/", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_value"]
        height = request.form["height_value"]
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            avg_height = db.session.query(func.avg(Data.height)).scalar()
            avg_height = round(avg_height, 2)
            count = db.session.query(Data.height).count()
            send_email(email, height, avg_height, count)
            return render_template("success.html")
        else:
            return render_template("index.html",
                                   text="Email address already has an entry")


if __name__ == "__main__":
    app.debug = True
    app.run()
