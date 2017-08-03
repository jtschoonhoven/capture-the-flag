import flask
import flask_login
from flask_restful import Api

from capture_the_flag import database as db
from capture_the_flag.models.user import load_user_from_session, User
from capture_the_flag.routes import files, index, login, logout, signup, users
from capture_the_flag.session import SuperSecureSessionInterface


# HACK: don't serve static files from the root path
app = flask.Flask(__name__)
api = Api(app)

app.config.from_object(__name__)
# HACK: this is a terrible secret key
app.config['SECRET_KEY'] = 'secret'
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024  # 256kb

# HACK: don't use compromised session interface
app.session_interface = SuperSecureSessionInterface()

# configure setup/teardown of DB connection
app.before_request(db.connect)
app.teardown_appcontext(db.close)

# initialize DB with an admin user
db.database.create_tables([User], safe=True)
User.get_or_create(
    username='admin',
    # HACK: don't hardcode admin credentials
    defaults={'username': 'admin', 'password': 'admin', 'file_access_path': '*'}
)

# configure login manager
login_manager = flask_login.LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in."
login_manager.init_app(app)
login_manager.user_loader(load_user_from_session)

# define routes
app.add_url_rule('/', 'index', index.handle_request)
app.add_url_rule('/login', 'login', login.handle_request, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout.handle_request)
app.add_url_rule('/signup', 'signup', signup.handle_request, methods=['GET', 'POST'])
app.add_url_rule('/users', 'users', users.handle_request)

app.add_url_rule(
    '/files/',
    'files',
    files.handle_request,
    defaults={'path': 'shared'},
    methods=['GET', 'POST'],
)
app.add_url_rule(
    '/files/<path:path>',
    'files',
    files.handle_request,
    methods=['GET', 'POST'],
)


if __name__ == '__main__':
    # HACK: never run an app in debug mode
    app.run(debug=True)
