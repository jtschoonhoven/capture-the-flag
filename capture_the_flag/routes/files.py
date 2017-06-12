import os

import flask
import flask_login


ROOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')


@flask_login.login_required
def handle_request(path):
    if flask.request.method == 'GET':
        return get(path)
    flask.flash('method not allowed')
    return flask.redirect(flask.url_for('index'))


def is_authorized(path):
    # HACK: this is a terrible way to do ACL
    user_path = flask_login.current_user.file_access_path
    if user_path == '*':
        return True
    path = path.strip('/').strip()
    user_path = user_path.strip('/').strip()
    return path.startswith(user_path)


def get(path):
    prefix_blacklist = frozenset(['.', '__init__'])
    suffix_blacklist = frozenset(['.pyc'])

    files = []
    directories = []

    abs_path = os.path.join(ROOT_PATH, path)
    if not os.path.exists(abs_path):
        flask.flash('file does not exist')
        abs_path = os.path.dirname(abs_path)

    path_urls = ['/files']
    for idx, part in enumerate(path.split('/')):
        if not part.strip():
            continue
        prev_url = path_urls[idx]
        path_urls.append(os.path.join(prev_url, part))

    if os.path.isfile(abs_path):
        # HACK: don't send any file on the server the user requests
        if is_authorized(path):
            return flask.send_file(abs_path)
        # if not authorized, redirect to parent dir
        flask.flash('you are not authorized to view that file')
        abs_path = os.path.dirname(abs_path)

    contents = os.listdir(abs_path)

    for item in contents:
        if any(item.startswith(prefix) for prefix in prefix_blacklist):
            continue
        if any(item.endswith(suffix) for suffix in suffix_blacklist):
            continue

        item_url = os.path.join(path_urls[-1], item)
        if os.path.isfile(os.path.join(abs_path, item)):
            files.append(item_url)
        else:
            directories.append(item_url)

    files.sort()
    directories.sort()

    return flask.render_template(
        'files.html',
        files=files,
        directories=directories,
        path_urls=path_urls,
        is_authorized=is_authorized(path),
    )
