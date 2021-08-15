import os
from PIL import Image

from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from my_flask import app, bcrypt, db, mail
from my_flask.forms import (
    AccountUpdateForm,
    ChangePasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
)
from my_flask.models import User, UserDetails


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=encrypted_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created successfuly for {form.username.data}", category="success"
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="SignUp", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data == user.email and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            flash(f"Entered successfully in {form.email.data}", category="success")
            return redirect(url_for("account"))
        else:
            flash(
                f"Invalid account email or password for {form.email.data}",
                category="danger",
            )
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


def save_account_image(image_file):
    image_name = image_file.filename
    image_path = os.path.join(app.root_path, "static/profile_images", image_name)

    # resize profile image using pillow module
    output_size = (125, 125)
    i = Image.open(image_file)
    i.thumbnail(output_size)

    i.save(image_path)
    return image_name


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.account_image.data:
            new_account_imagefile_name = save_account_image(form.account_image.data)
            current_user.profile_image = new_account_imagefile_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        user_details = UserDetails(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            user_id=current_user.id,
        )
        db.session.add(user_details)
        db.session.commit()
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.first_name.data = current_user.details[-1].first_name
        form.last_name.data = current_user.details[-1].last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_url = url_for(
        "static", filename="profile_images/" + current_user.profile_image
    )
    flash(f"Account info updated successfully", category="success")
    return render_template(
        "account.html",
        title="Account",
        legend="Account details",
        form=form,
        image_url=image_url,
    )


def send_email(user):
    print(type(user))
    token = user.get_token()
    msg = Message(
        subject="Reset password",
        recipients=[user.email],
        sender="noreply@gmail.com",
        body=f""" To reser your password follow the link below

    .....

    {url_for('reset_token', token=token, _external=True)}

    If you didn't sent a password reset request please ignore this message

    
    
    
     """,
    )
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash("Reset request is sent. Check your mail", category="success")
            return redirect(url_for("login"))
    return render_template(
        "reset_pass.html", title="Reset password", form=form, legend="Reset password"
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash("That token is invalid or expired. Please try again", "warning")
        redirect(url_for("reset_password"))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(
            form.new_password.data
        ).decode("utf-8")
        user.password = encrypted_password
        db.session.commit()
        flash("Password has been changed successfully. Please login", "success")
        return redirect(url_for("login"))
    return render_template(
        "change_password.html",
        title="Change password",
        legend="Change password",
        form=form,
    )


@app.route("/customers")
def customers():
    return render_template("customers.html", title="Customers")


@app.route("/projects")
def projects():
    return render_template("projects.html", title="Projects")
