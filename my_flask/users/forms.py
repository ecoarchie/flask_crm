from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    first_name = StringField(
        label="First name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    last_name = StringField(
        label="Last name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=6, max=60)]
    )
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(label="SignUp")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=6, max=60)]
    )
    submit = SubmitField(label="Login")


class ResetPasswordForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label="Reset password")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField(
        label="New password", validators=[DataRequired(), Length(min=6, max=60)]
    )
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField(label="Confirm")


class AccountUpdateForm(FlaskForm):
    first_name = StringField(
        label="First name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    last_name = StringField(
        label="Last Name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    account_image = FileField(
        label="Update account image", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Update Account")
