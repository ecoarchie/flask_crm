from datetime import datetime
from enum import unique

from flask import redirect, url_for, current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref

from my_flask import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("users.register"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False, default="user")
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(
        db.String(60), nullable=False
    )  # bcrypt encrypts password to 60 characters long
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    leads = db.relationship("Customer", backref="manager", lazy=True)
    deals = db.relationship("Deal", backref="owner", lazy=True)
    notes = db.relationship("CustomerNotes", backref="author", lazy=True)

    def get_token(self, expires_sec=300):
        serial = Serializer(
            secret_key=current_app.config["SECRET_KEY"], expires_in=expires_sec
        )
        return serial.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_token(token):
        serial = Serializer(secret_key=current_app.config["SECRET_KEY"])
        try:
            user_id = serial.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.first_name} : {self.last_name} : {self.email}"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=True)
    status = db.Column(db.String(20), unique=False, nullable=False, default="NEW")
    company = db.Column(db.String(20), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    deals = db.relationship("Deal", backref="manager", lazy=True)
    notes = db.relationship("CustomerNotes", backref="customer", lazy=True)


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    customer = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class CustomerNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text, nullable=False, unique=False)
    note_type = db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
