from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import text # does this help?

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///tmalin"
db = SQLAlchemy(app)

@app.route("/")
def index():
#    result = db.session.execute("SELECT content FROM messages")
    result = db.session.execute("SELECT category FROM categories")
    #messages = result.fetchall()
    categories = result.fetchall()
    return render_template("index.html", count=len(categories), categories=categories) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    category = request.form["category"]
    sql = "INSERT INTO categories (category) VALUES (:category)"
    db.session.execute(sql, {"category":category})
    db.session.commit()
    return redirect("/")
