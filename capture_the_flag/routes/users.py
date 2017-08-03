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
    conditions = []
    # HACK: accepting arbitrary query params is never a good idea
    for field, value in flask.request.args.iteritems():
        condition = '{} = \'{}\''.format(field, value)
        conditions.append(condition)

    conditions_str = 'WHERE {}'.format('\nAND'.join(conditions)) if conditions else ''

    # HACK: SQL-injection vulnerability
    queries = '''
        SELECT id, username, file_access_path
        FROM users
        {conditions}
        ORDER BY id ASC
        LIMIT 10
    '''.format(conditions=conditions_str)

    # HACK: this doesn't even make sense except to make injection easier
    for query in queries.split(';'):
        if query:
            users = db.fetch_all(query)
    return flask.render_template('users.html', users=users)
