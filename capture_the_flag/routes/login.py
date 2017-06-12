import flask
import flask_login
from peewee import DoesNotExist

from capture_the_flag.models.user import User


def handle_request():
    if flask.request.method == 'GET':
        return get()
    if flask.request.method == 'POST':
        return post()
    flask.flash('method not allowed')
    return flask.redirect(flask.url_for('index'))


def get():
    if flask_login.current_user.is_authenticated:
        flask.flash('already logged in')
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('login.html')


def post():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    remember = flask.request.form.get('remember', False)

    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        # HACKABLE: don't say "user does not exist", this is a way to learn which
        # users DO exist (e.g. "admin")
        flask.flash('user does not exist')
        return flask.render_template('login.html')

    if user.password != password:
        flask.flash('wrong password')
        return flask.render_template('login.html')

    flask_login.login_user(user, remember=remember)
    flask.flash('logged in successfully')
    return flask.redirect(flask.url_for('files'))
