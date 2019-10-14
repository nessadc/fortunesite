from flask import render_template, flash, redirect
from fortunesite import app
from fortunesite.forms import LoginForm, SubmitForm

fortune = "You will live a long and healthy life"


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html", fortune=fortune)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
    return render_template('login.html', title='Log In', form=form)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    return render_template('create_fortune.html', title='New Fortune', form=form)