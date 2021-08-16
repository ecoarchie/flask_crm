from dotenv import load_dotenv
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


app.config["SECRET_KEY"] = "mysecretkey"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/flaskapp"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("GMAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_PASSWORD")


mail = Mail(app)

from my_flask.users.routes import users
from my_flask.main.routes import main
from my_flask.customers.routes import customers

app.register_blueprint(users)
app.register_blueprint(customers)
app.register_blueprint(main)
