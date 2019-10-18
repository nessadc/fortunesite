from flask import render_template, flash, redirect, url_for, request
from fortunesite import app, db
from fortunesite.forms import LoginForm, SubmitForm, RegistrationForm
from fortunesite.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


fortune = "You will live a long and healthy life"


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html", fortune=fortune)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        flash('New fortune submitted!')
    return render_template('create_fortune.html', title='New Fortune',
                           form=form)
