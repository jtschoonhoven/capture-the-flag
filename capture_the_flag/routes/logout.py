import flask
import flask_login


def handle_request():
    if flask.request.method == 'GET':
        return get()
    flask.flash('method not allowed')
    return flask.redirect(flask.url_for('index'))


@flask_login.login_required
def get():
    flask_login.logout_user()
    flask.flash('Logged out successfully.')
    return flask.redirect(flask.url_for('index'))
