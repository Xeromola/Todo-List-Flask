from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todo_list import config
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(config.Config)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login_page'

from todo_list import routes, models