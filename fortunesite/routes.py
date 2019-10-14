from flask import render_template
from fortunesite import app
from fortunesite.forms import SubmitForm

fortune = "You will live a long and healthy life"


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html", fortune=fortune)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    return render_template('create_fortune.html', title='New Fortune',
                            form=form)