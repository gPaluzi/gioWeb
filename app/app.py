import json
from flask import Flask, render_template

def load_about_data():
    with open("./app/data/about.json") as f:
        return json.load(f)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    data = load_about_data()
    return render_template("about.html", about = data)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

if __name__ == "__main__":
    app.run(debug=True)