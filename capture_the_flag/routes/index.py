import flask
import flask_login


def handle_request():
    if flask.request.method == 'GET':
        return get()
    flask.flash('method not allowed')
    return flask.redirect(flask.url_for('index'))


def get():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('files'))
    return flask.render_template('index.html')
