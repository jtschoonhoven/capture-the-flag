import os

import flask
import flask_login
from typing import List  # noqa

from capture_the_flag.constants import ROOT_PATH


@flask_login.login_required
def handle_request(path):
    # type: (str) -> str
    if flask.request.method == 'GET':
        return get(path)
    if flask.request.method == 'POST':
        return post(path)

    flask.flash('method not allowed')
    return flask.redirect(flask.url_for('index'))


def post(path):
    # type: (str) -> str
    file = flask.request.files.get('file')

    if not file or not file.filename:
        flask.flash('request did not contain a file')
        return flask.redirect(flask.request.url)

    if not is_authorized(path):
        flask.flash('you are not authorized to upload to this directory')
        return flask.redirect(flask.request.url)

    # HACK: always whitelist file extensions for uploads
    # HACK: always use werkzeug.utils.secure_filename to sanitize file names
    abs_path = os.path.join(ROOT_PATH, path, file.filename)

    try:
        file.save(abs_path)
    except Exception as e:
        # HACK: don't display raw error message to user
        flask.flash('upload failed: "{}"'.format(str(e)))

    flask.flash('Upload successful.')
    return flask.redirect(flask.request.url)


def get(path):
    # type: (str) -> str
    prefix_blacklist = frozenset(['.', '__init__'])
    suffix_blacklist = frozenset(['.pyc'])

    files = []  # type: List[str]
    directories = []  # type: List[str]

    # translate URL to local filesystem path and ensure exists
    abs_path = os.path.join(ROOT_PATH, path)
    if not os.path.exists(abs_path):
        flask.flash('file or directory "{}" does not exist'.format(path))
        return flask.redirect(flask.url_for('files'))

    # break URL path into parts for breadcrumbs
    path_urls = ['/files']
    for idx, part in enumerate(path.split('/')):
        if not part.strip():
            continue
        prev_url = path_urls[idx]
        path_urls.append(os.path.join(prev_url, part))

    # if URL path is file, send file (if authorized)
    if os.path.isfile(abs_path):
        # HACK: don't send any file on the server the user requests
        if is_authorized(path):
            return flask.send_file(abs_path)
        # if not authorized, redirect to parent dir
        flask.flash('you are not authorized to view that file')
        return flask.redirect(path_urls[-2])

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


def is_authorized(path):
    # type: (str) -> bool
    # HACK: this is a terrible way to do ACL
    user_path = flask_login.current_user.file_access_path

    if user_path == '*':
        return True
    if 'private' in path:
        return False
    return True
