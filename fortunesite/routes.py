# my pages are defined here
from flask import render_template
from fortunesite import app

fortune = "You will live a long and healthy life"


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html", fortune=fortune)


@app.route('/about')
def about():
    return render_template("about.html")
