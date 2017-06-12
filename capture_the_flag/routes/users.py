import flask
import flask_login

from capture_the_flag import database as db


@flask_login.login_required
def handle_request():
    if flask.request.method == 'GET':
        return get()
    flask.flash('method not allowed')
    return flask.redirect(flask.url_for('index'))


def get():
    offset = flask.request.args.get('offset', 0)
    sort = flask.request.args.get('sort', 'ASC')
    limit = flask.request.args.get('limit', 10)

    # HACK: SQL-injection vulnerability
    users = db.fetch_all('''
        SELECT id, username, file_access_path
        FROM users
        WHERE id >= {offset}
        ORDER BY id {sort}
        LIMIT {limit}
        '''.format(offset=offset, sort=sort, limit=limit)
    )
    return flask.render_template('users.html', users=users)
