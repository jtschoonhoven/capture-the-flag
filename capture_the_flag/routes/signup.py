import flask
import flask_login
from peewee import IntegrityError

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
    return flask.render_template('signup.html')


def post():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    remember = flask.request.form.get('remember', False)

    try:
        # this should really validate stuff but w/e
        user = User.create(username=username, password=password)
    except IntegrityError:
        flask.flash('user already exists')
        return flask.render_template('signup.html')

    flask_login.login_user(user, remember=remember)
    flask.flash('signud up successfully')
    return flask.redirect(flask.url_for('index'))

    return flask.render_template('signup.html')
