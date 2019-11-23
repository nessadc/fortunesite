import random
from datetime import datetime

from flask import flash, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from fortunesite import db
from fortunesite.main import bp
from fortunesite.main.forms import EditProfileForm, FortuneForm, SearchForm
from fortunesite.models import Fortune, User


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()

@bp.route('/index')
@bp.route('/')
def index():
    try:
        fortune = random.choice(Fortune.query.all())
    except IndexError:
        fortune = None
    return render_template("index.html", fortune=fortune)


@bp.route('/about')
def about():
    return render_template("about.html")


@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = FortuneForm()
    if form.validate_on_submit():
        fortune = Fortune(content=form.content.data, author=current_user)
        db.session.add(fortune)
        db.session.commit()
        flash('New fortune submitted!')
        return redirect(url_for('main.submit'))
    return render_template('create_fortune.html', title='New Fortune',
                           form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    fortunes = Fortune.query.filter_by(author=user).all()
    return render_template('user.html', user=user, fortunes=fortunes)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/delete/<fortune_id>')
@login_required
def delete(fortune_id):
    Fortune.query.filter_by(id=fortune_id).delete()
    db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    fortunes, total = Fortune.search(g.search_form.q.data, page, 10)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * 10 else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=('Search'), fortunes=fortunes,
                            next_url=next_url, prev_url=prev_url)
