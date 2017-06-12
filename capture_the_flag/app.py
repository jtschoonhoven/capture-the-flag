import flask
import flask_login
from flask_restful import Api

from capture_the_flag import database as db
from capture_the_flag.models.user import load_user_from_session, User
from capture_the_flag.session import SuperSecureSessionInterface
from capture_the_flag.routes import files, index, login, logout, signup


# HACK: don't serve static files from the root path
app = flask.Flask(__name__, static_folder='.', static_url_path='/')
api = Api(app)

app.config.from_object(__name__)
# HACK: this is a terrible secret key
app.config['SECRET_KEY'] = 'secret'

# HACK: don't use compromised session interface
app.session_interface = SuperSecureSessionInterface()

app.before_request(db.connect)
app.teardown_appcontext(db.close)

db.database.create_tables([User], safe=True)
User.get_or_create(
    username='admin',
    defaults={'username': 'admin', 'password': 'admin', 'file_access_path': '*'}
)

login_manager = flask_login.LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in."
login_manager.init_app(app)
login_manager.user_loader(load_user_from_session)

app.add_url_rule('/', 'index', index.handle_request)
app.add_url_rule('/login', 'login', login.handle_request, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout.handle_request)
app.add_url_rule('/signup', 'signup', signup.handle_request, methods=['GET', 'POST'])
app.add_url_rule('/files/', 'files', files.handle_request, defaults={'path': 'shared'})
app.add_url_rule('/files/<path:path>', 'files', files.handle_request)


if __name__ == '__main__':
    app.run(debug=True)
