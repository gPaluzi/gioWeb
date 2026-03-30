import json
from flask import Flask, render_template
from sqlalchemy import select
from models import Experience
from database import db_session
from collections import defaultdict

def load_about_data():
    with open("./app/data/about.json") as f:
        return json.load(f)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    query = select(Experience).order_by(Experience.start_date.desc())
    result = db_session.execute(query)

    data = defaultdict(list)
    for exp in result.scalars():
        data[exp.category].append(exp)

    about = load_about_data()
    
    return render_template("about.html", about = about, data = data)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

if __name__ == "__main__":
    app.run(debug=True)