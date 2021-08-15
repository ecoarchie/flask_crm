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

GMAIL_SERVER = os.getenv("GMAIL_SERVER")
GMAIL_PORT = os.getenv("GMAIL_PORT")
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


app.config["MAIL_SERVER"] = GMAIL_SERVER
app.config["MAIL_PORT"] = GMAIL_PORT
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = GMAIL_USERNAME
app.config["MAIL_PASSWORD"] = GMAIL_PASSWORD


mail = Mail(app)

from my_flask import routes
