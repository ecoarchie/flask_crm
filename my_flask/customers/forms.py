from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class AddCustomerForm(FlaskForm):
    first_name = StringField(
        label="First name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    last_name = StringField(
        label="Last name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    status = StringField(
        label="Status", validators=[DataRequired(), Length(min=3, max=20)]
    )
    company = StringField(
        label="Company", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label="Add customer")
