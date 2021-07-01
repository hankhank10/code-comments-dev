from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from flask_admin import Admin
from flask_admin.contrib import sqla
from sqlalchemy.sql.expression import false, true

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

#def create_app():
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codecomments.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#login_manager = LoginManager()
#login_manager.login_view = 'auth.login'
#login_manager.init_app(app)

# Set the main URL
website_url = ""

# db init
#from .models import User
from .models import Snapshot
from .models import Gist
from .models import Line
from .models import Comment


db.init_app(app)
migrate = Migrate(app, db)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))


# blueprints
#from .auth import auth as auth_blueprint
#app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .loader import loader as loader_blueprint
app.register_blueprint(loader_blueprint)

from .gists import gists as gists_blueprint
app.register_blueprint(gists_blueprint)

from .comments import comments as comments_blueprint
app.register_blueprint(comments_blueprint)

#
# Flask admin

# Create customized model view class
#class MyModelView(sqla.ModelView):
#    def is_accessible(self):
#
#        if current_user.is_authenticated:
#            return current_user.is_superuser
#        return False


#admin = Admin(app, name='CodeComments Admin', template_mode='bootstrap3')

#admin.add_view(MyModelView(User, db.session))







