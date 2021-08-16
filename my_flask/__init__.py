from my_flask.errors.handlers import error_404
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from my_flask.config import Config

load_dotenv()


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from my_flask.users.routes import users
    from my_flask.main.routes import main
    from my_flask.customers.routes import customers
    from my_flask.projects.routes import projects
    from my_flask.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(customers)
    app.register_blueprint(main)
    app.register_blueprint(projects)
    app.register_blueprint(errors)

    return app
